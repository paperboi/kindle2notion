import bisect
from datetime import datetime
from typing import Optional, cast
import notional
from notional.blocks import Paragraph, Quote, Page, Heading2
from notional.query import TextCondition
from notional.types import Date, ExternalFile, Number, RichText, Title, Checkbox
from kindle2notion import models
from kindle2notion.reading import find_mobi_file, MobiHandler
from kindle2notion.package_logger import logger
from requests import get
from fuzzysearch import find_near_matches

NO_COVER_IMG = "https://via.placeholder.com/150x200?text=No%20Cover"


def export_to_notion(
    all_books: dict[str, models.Book],
    enable_location: bool,
    enable_highlight_date: bool,
    enable_book_cover: bool,
    separate_blocks: bool,
    notion_api_auth_token: str,
    notion_database_id: str,
    kindle_root: Optional[str],
) -> None:
    logger.info("Initiating transfer...\n")

    for book in all_books.values():
        try:
            message = _add_book_to_notion(
                book,
                notion_api_auth_token,
                notion_database_id,
                enable_book_cover,
                separate_blocks,
                enable_location,
                enable_highlight_date,
                kindle_root=kindle_root,
            )
            if message:
                logger.info(f"[green]✓[/green] {message}")
            else:
                logger.info("Nothing to add!")
        except Exception as e:
            logger.error(f"An error occured in writing: {book.title} ({book.author})")
            raise e


def get_heading_info(
    book: models.Book, kindle_root: str
) -> tuple[list[models.BookHeading], list[Optional[int]]]:
    """
    Given a book, this will return a tuple
    (l1, l2)
    l1 -> list of all headings
    l2 -> list of indices into l1 for each highlight in the book such that the highlight comes under that particular heading
    """
    headings = []
    indices: list[Optional[int]] = [None for _ in range(len(book.highlights))]

    mobi_path = find_mobi_file(book, kindle_root)
    if mobi_path is None:
        return headings, indices
    mobi_handler = MobiHandler(mobi_path)
    try:
        headings = mobi_handler.process()
    except Exception as e:
        logger.error("An error occured in handling the mobi file", exc_info=True)
        return headings, indices
    headings = [h for h in headings if h.position != -1]
    if len(headings) == 0:
        logger.error(
            "Could not extract positions for any heading, or no headings were found at all"
        )
        return headings, indices
    headings = sorted(headings, key=lambda x: x.position)

    assert mobi_handler.html_file_path is not None
    html_str = open(mobi_handler.html_file_path, "r", errors="ignore").read()
    for i, highlight in enumerate(book.highlights):
        # NOTE: arbitrary first 50 characters
        txt_short = highlight.text[:50].strip()
        # txt_pos = html_str.find(txt_short)
        # NOTE: allowing for a 4% error tolerance here
        matches = find_near_matches(txt_short, html_str, max_l_dist=2)
        if len(matches) == 0:
            logger.warning(
                f"Failed to find text in html:\n [italic]{txt_short}[/italic]"
            )
            continue
        txt_pos = matches[0].start
        heading_pos = bisect.bisect_right(headings, txt_pos, key=lambda x: x.position)
        if heading_pos != 0:
            indices[i] = heading_pos - 1
    return (headings, indices)


def _write_to_page(
    notion: notional.session.Session,
    page_block: Page,
    separate_blocks: bool,
    book: models.Book,
    enable_location: bool,
    enable_highlight_date: bool,
    kindle_root: Optional[str],
):
    headings = []
    highlight_to_heading_indices = [None for _ in range(len(book.highlights))]

    if kindle_root:
        headings, highlight_to_heading_indices = get_heading_info(book, kindle_root)

    formatted_clippings = [
        h.make_aggregate_text(
            enable_location=enable_location, enable_highlight_date=enable_highlight_date
        )
        for h in book.highlights
    ]
    if separate_blocks:
        page_contents = []
        last_heading_idx = None
        for heading_idx, clip in zip(highlight_to_heading_indices, formatted_clippings):
            if len(page_contents) >= 99:
                notion.blocks.children.append(page_block, *page_contents)
                page_contents = []
            if heading_idx is not None and last_heading_idx != heading_idx:
                page_contents.append(Heading2[headings[heading_idx].title.strip()])
                last_heading_idx = heading_idx

            page_contents.append(Quote[clip.strip()])

        notion.blocks.children.append(page_block, *page_contents)

    else:
        # TODO: Special case for books with len(clippings) >= 100 characters. Character limit in a Paragraph block in Notion is 100
        page_content = Paragraph["".join(formatted_clippings)]
        notion.blocks.children.append(page_block, page_content)


def _add_book_to_notion(
    book: models.Book,
    notion_api_auth_token: str,
    notion_database_id: str,
    enable_book_cover: bool,
    separate_blocks: bool,
    enable_location: bool,
    enable_highlight_date: bool,
    kindle_root: Optional[str],
) -> Optional[str]:
    notion = notional.connect(auth=notion_api_auth_token)

    query = (
        notion.databases.query(notion_database_id)
        .filter(property="Title", rich_text=TextCondition(equals=book.title))
        .limit(1)
    )
    page_block: Page = cast(Page, query.first())
    needs_writing: bool = False

    title_and_author = book.title + " (" + str(book.author) + ")"
    logger.info(title_and_author)
    logger.info("-" * len(title_and_author))

    if page_block:
        last_highlighted_dt = cast(
            datetime,
            page_block.properties["Last Highlighted"].date.start or datetime.min,
        )
        blockquoted = cast(bool, page_block.properties["Blockquoted"].checkbox)
        includes_location = cast(
            bool, page_block.properties["Includes Location"].checkbox
        )
        includes_timestamp = cast(
            bool, page_block.properties["Includes Timestamp"].checkbox
        )
        current_highlight_count = page_block.properties["Highlights"].number or 0

        needs_writing = (
            (
                last_highlighted_dt.replace(second=0, tzinfo=None)
                < book.last_highlighted_date.replace(second=0, tzinfo=None)
            )
            | (includes_location ^ enable_location)
            | (includes_timestamp ^ enable_highlight_date)
            | (blockquoted ^ separate_blocks)
            | (current_highlight_count != len(book.highlights))
        )

    else:
        needs_writing = True

    if not needs_writing:
        return

    # Clear the contents of the existing page if we are rewriting.
    if page_block:
        notion.pages.delete(page_block)

    # Create a brand new page block with the correct properties
    page_block = notion.pages.create(
        parent=notion.databases.retrieve(notion_database_id),
        properties={
            "Title": Title[book.title],
            "Author": RichText[book.author],
            "Last Highlighted": Date[book.last_highlighted_date.isoformat()],
            "Blockquoted": Checkbox[separate_blocks],
            "Includes Location": Checkbox[enable_location],
            "Includes Timestamp": Checkbox[enable_highlight_date],
        },
        children=[],
    )

    if enable_book_cover:
        # Fetch a book cover from Google Books if the cover for the page is not set
        if page_block.cover is None:
            result = _get_book_cover_uri(book.title, book.author)

        if result is None:
            # Set the page cover to a placeholder image
            cover = ExternalFile[NO_COVER_IMG]
            logger.error(
                "[red]×[/red] Book cover couldn't be found. "
                "Please replace the placeholder image with the original book cover manually."
            )
        else:
            # Set the page cover to that of the book
            cover = ExternalFile[result]
            logger.info("[green]✓[/green] Added book cover.")

        notion.pages.set(page_block, cover=cover)
    try:
        _write_to_page(
            notion=notion,
            page_block=page_block,
            separate_blocks=separate_blocks,
            book=book,
            enable_location=enable_location,
            enable_highlight_date=enable_highlight_date,
            kindle_root=kindle_root,
        )
        # Only write this once content has been succesfully written to page
        notion.pages.update(
            page_block,
            **{
                "Highlights": Number[len(book.highlights)],
                "Last Synced": Date[datetime.now().isoformat()],
            },
        )
        return str(len(book.highlights)) + " notes/highlights added successfully.\n"
    except Exception as e:
        logger.error("Failed writing to notion")
        notion.pages.delete(page_block)
        raise e


# def _create_rich_text_object(text):
#     if "Note: " in text:
#         # Bold text
#         nested = TextObject._NestedData(content=text)
#         rich = TextObject(text=nested, plain_text=text, annotations=Annotations(bold=True))
#     elif any(item in text for item in ["Page: ", "Location: ", "Date Added: "]):
#         # Italic text
#         nested = TextObject._NestedData(content=text)
#         rich = TextObject(text=nested, plain_text=text, annotations=Annotations(italic=True))
#     else:
#         # Plain text
#         nested = TextObject._NestedData(content=text)
#         rich = TextObject(text=nested, plain_text=text)
#     return rich


# def _update_book_with_clippings(formatted_clippings):
#     rtf = []
#     for each_clipping in formatted_clippings:
#         each_clipping_list = each_clipping.split("*")
#         each_clipping_list = list(filter(None, each_clipping_list))
#         for each_line in each_clipping_list:
#             rtf.append(_create_rich_text_object(each_line))
#     print(len(rtf))
#     content = Paragraph._NestedData(rich_text=rtf)
#     para = Paragraph(paragraph=content)
#     return para


def _get_book_cover_uri(title: str, author: str):
    req_uri = "https://www.googleapis.com/books/v1/volumes?q="

    if title is None:
        return
    req_uri += "intitle:" + title

    if author is not None:
        req_uri += "+inauthor:" + author

    response = get(req_uri).json().get("items", [])
    if len(response) > 0:
        for x in response:
            if x.get("volumeInfo", {}).get("imageLinks", {}).get("thumbnail"):
                return (
                    x.get("volumeInfo", {})
                    .get("imageLinks", {})
                    .get("thumbnail")
                    .replace("http://", "https://")
                )
    return
