from datetime import datetime

import pydantic
from kindle2notion import models
from re import findall
from typing import Dict, List, Optional, Tuple
from dateparser import parse
from kindle2notion.package_logger import logger

BOOKS_WO_AUTHORS = []

ACADEMIC_TITLES = [
    "A.A.",
    "A.S.",
    "A.A.A.",
    "A.A.S.",
    "A.B.",
    "A.D.N.",
    "A.M.",
    "A.M.T.",
    "C.E.",
    "Ch.E.",
    "D.A.",
    "D.A.S.",
    "D.B.A.",
    "D.C.",
    "D.D.",
    "D.Ed.",
    "D.L.S.",
    "D.M.D.",
    "D.M.S.",
    "D.P.A.",
    "D.P.H.",
    "D.R.E.",
    "D.S.W.",
    "D.Sc.",
    "D.V.M.",
    "Ed.D.",
    "Ed.S.",
    "E.E.",
    "E.M.",
    "E.Met.",
    "I.E.",
    "J.D.",
    "J.S.D.",
    "L.H.D.",
    "Litt.B.",
    "Litt.M.",
    "LL.B.",
    "LL.D.",
    "LL.M.",
    "M.A.",
    "M.Aero.E.",
    "M.B.A.",
    "M.C.S.",
    "M.D.",
    "M.Div.",
    "M.E.",
    "M.Ed.",
    "M.Eng.",
    "M.F.A.",
    "M.H.A.",
    "M.L.S.",
    "M.Mus.",
    "M.N.",
    "M.P.A.",
    "M.S.",
    "M.S.Ed.",
    "M.S.W.",
    "M.Th.",
    "Nuc.E.",
    "O.D.",
    "Pharm.D.",
    "Ph.B.",
    "Ph.D.",
    "S.B.",
    "Sc.D.",
    "S.J.D.",
    "S.Sc.D.",
    "Th.B.",
    "Th.D.",
    "Th.M.",
]

DELIMITERS = ["; ", " & ", " and "]


def parse_raw_clippings_text(raw_clippings_text: str) -> Dict:
    raw_clippings_list = raw_clippings_text.split("==========")
    logger.info(
        f"Found [white on yellow]{len(raw_clippings_list)}[/white on yellow] notes and highlights.\n"
    )

    all_books: dict[str, models.Book] = {}
    passed_clippings_count = 0

    for each_raw_clipping in raw_clippings_list:
        raw_clipping_list = each_raw_clipping.strip().split("\n")

        if _is_valid_clipping(raw_clipping_list):
            author, title = _parse_author_and_title(raw_clipping_list)
            page, location, date, is_note = _parse_page_location_date_and_note(
                raw_clipping_list
            )
            highlight = raw_clipping_list[3]

            if title not in all_books:
                all_books[title] = models.Book(
                    title=title, author=author, highlights=[]
                )
            try:
                highlight_pyd = models.Highlight(
                    text=highlight,
                    page=page,
                    location=location,
                    date=date,
                    is_note=is_note,
                )
                all_books[title].highlights.append(highlight_pyd)
            except pydantic.ValidationError:
                passed_clippings_count += 1

        else:
            passed_clippings_count += 1

    logger.warning(
        f"[red]×[/red] Parsed {passed_clippings_count} bookmarks or unsupported clippings.\n"
    )

    # Clear empty books
    for book_title in list(all_books.keys()):
        if len(all_books[book_title].highlights) == 0:
            del all_books[book_title]

    # Prune highlights for every book
    for book_info in all_books.values():
        book_info.prune_subset_highlights()

    return all_books


def _is_valid_clipping(raw_clipping_list: List) -> bool:
    return len(raw_clipping_list) >= 3


def _parse_author_and_title(raw_clipping_list: List) -> Tuple[str, str]:
    author, title = _parse_raw_author_and_title(raw_clipping_list)
    author, title = _deal_with_exceptions_in_author_name(author, title)
    title = _deal_with_exceptions_in_title(title)
    return author, title


def _parse_page_location_date_and_note(
    raw_clipping_list: List,
) -> Tuple[Optional[int], Optional[tuple[int, int]], Optional[datetime], bool]:
    second_line = raw_clipping_list[1]
    second_line_as_list = second_line.strip().split(" | ")

    page = None
    location = None
    date = None
    is_note = False

    for element in second_line_as_list:
        element = element.lower()
        if "note" in element:
            is_note = True
        if "page" in element:
            page = element[element.find("page") :].replace("page", "").strip()
            try:
                page = int(page)
            except ValueError:
                page = None
        if "location" in element:
            location = (
                element[element.find("location") :].replace("location", "").strip()
            )
            try:
                location = (
                    int(location.split("-")[0]),
                    int(location.split("-")[1]),
                )
            except (ValueError, IndexError):
                location = None
        if "added on" in element:
            date = parse(
                element[element.find("added on") :].replace("added on", "").strip()
            )

    return page, location, date, is_note


def _parse_raw_author_and_title(raw_clipping_list: List) -> Tuple[str, str]:
    author = ""
    title = raw_clipping_list[0]

    if findall(r"\(.*?\)", raw_clipping_list[0]):
        author = (findall(r"\(.*?\)", raw_clipping_list[0]))[-1]
        author = author.removeprefix("(").removesuffix(")")
    else:
        if title not in BOOKS_WO_AUTHORS:
            BOOKS_WO_AUTHORS.append(title)
            logger.warning(
                f"{title} - No author found. You can manually add the author in the Notion database."
            )

    title = raw_clipping_list[0].replace(author, "").strip().replace(" ()", "")

    return author, title


def _deal_with_exceptions_in_author_name(author: str, title: str) -> Tuple[str, str]:
    if "(" in author:
        author = author + ")"
        title = title.removesuffix(")")

    if ", " in author and all(x not in author for x in DELIMITERS):
        if (author.split(", "))[1] not in ACADEMIC_TITLES:
            author = " ".join(reversed(author.split(", ")))

    if "; " in author:
        authorList = author.split("; ")
        author = ""
        for ele in authorList:
            author += " ".join(reversed(ele.split(", "))) + ", "
        author = author.removesuffix(", ")
    return author, title


def _deal_with_exceptions_in_title(title: str) -> str:
    if ", The" in title:
        title = "The " + title.replace(", The", "")
    return title
