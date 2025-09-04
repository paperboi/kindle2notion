import glob
import os
import shutil
import mobi
from pathlib import Path
from typing import Optional
import re
from urllib.parse import unquote
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings

from kindle2notion import models
from kindle2notion.package_logger import logger

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def read_raw_clippings(clippings_file_path: Path) -> str:
    try:
        with open(clippings_file_path, "r", encoding="utf-8-sig") as raw_clippings_file:
            raw_clippings_text = raw_clippings_file.read()
        raw_clippings_text = raw_clippings_text.replace("\ufeff", "")
        raw_clippings_text_decoded = raw_clippings_text.encode(
            "ascii", errors="ignore"
        ).decode()
    except UnicodeEncodeError as e:
        logger.error("Error in reading raw clippings", exc_info=True)

    return raw_clippings_text_decoded


def remove_special_characters(text):
    # Replace all non-alphanumeric characters with an empty string
    return re.sub(r"[^A-Za-z0-9]", "", text)


def _preformat(text: str):
    return remove_special_characters(text.lower().strip())


def find_mobi_file(book: models.Book, kindle_root: str) -> Optional[str]:
    all_books = glob.glob(os.path.join(kindle_root, "**/*.mobi"))
    for search_by in [book.title, book.author]:
        search_by = _preformat(search_by)
        logger.info(
            f"Searching mobi file with keyword: [white on dodger_blue1]{search_by}[/white on dodger_blue1]"
        )
        matching_books = [x for x in all_books if search_by in _preformat(x)]
        if len(matching_books) == 1:
            return matching_books[0]
        else:
            logger.warning(
                f"Attempt to search failed. Matching candidates: {matching_books}"
            )


class MobiHandler:
    # --- Build TOC positions by locating anchors in the raw HTML string ---
    ANCHOR_RE_TEMPLATE = r'(?i)\b(?:id|name)\s*=\s*([\'"])%s\1'

    def __init__(self, path: str) -> None:
        self.path = path
        # tuple of (parent directory, html file path)
        self.html_dir: Optional[str]
        self.html_file_path: Optional[str]
        self.toc_entries: Optional[list[models.BookHeading]]

    def process(self) -> list[models.BookHeading]:
        """
        Will raise an exception if something went wrong
        """
        self.extract_to_html()
        self.parse_toc_ncx()
        self.build_toc_positions_for_html()
        assert self.toc_entries is not None
        return self.toc_entries

    def extract_to_html(self):
        try:
            self.html_dir, self.html_file_path = mobi.extract(self.path)
        except Exception as e:
            logger.error("An error occured in extraction to html")
            raise e

    # --- Parse toc.ncx with html.parser ---
    def parse_toc_ncx(self):
        assert self.html_dir is not None, "No html dir found, aborting"
        # FIXME: hardcoding mobi7 for now
        ncx_path = os.path.join(self.html_dir, "mobi7", "toc.ncx")
        with open(ncx_path, "r", errors="ignore") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        entries = []
        for np in soup.find_all("navpoint"):
            # <navPoint><navLabel><text>Title</text></navLabel><content src="chapter.html#anchor"/></navPoint>
            label_wrap = np.find("navlabel")
            label_tag = label_wrap.find("text") if label_wrap else None
            content_tag = np.find("content")
            if label_tag and content_tag and content_tag.get("src"):
                title = label_tag.get_text(strip=True)
                href = content_tag["src"]
                entries.append(models.BookHeading(**{"title": title, "href": href}))

        self.toc_entries = entries

    def build_toc_positions_for_html(self):
        """
        Returns sorted list of (title, index) for toc entries that point into this html_str.
        If toc href has a different filename than current_filename, it's ignored here.
        """
        assert self.toc_entries is not None and len(self.toc_entries) > 0, (
            "no toc found, skipping title matching"
        )
        assert self.html_file_path is not None, (
            "converted html file not found, skipping title matching"
        )

        html_str = open(self.html_file_path, "r", errors="ignore").read()
        current_filename = os.path.basename(self.html_file_path)

        for e in self.toc_entries:
            href = e.href
            file_part = None
            frag = None
            if "#" in href:
                file_part, frag = href.split("#", 1)
            else:
                file_part = href
                frag = None

            # If the TOC points to a different file, skip (or load that file separately).
            if file_part and current_filename and file_part != current_filename:
                continue

            if frag:
                anchor = unquote(frag)
                # Match id="anchor" or name="anchor" in any tag
                pattern = re.compile(self.ANCHOR_RE_TEMPLATE % re.escape(anchor))
                m = pattern.search(html_str)
                if m:
                    e.position = m.start()

    def __del__(self):
        if self.html_dir is not None and os.path.exists(self.html_dir):
            shutil.rmtree(self.html_dir)
