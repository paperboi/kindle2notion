from datetime import datetime
from typing import Dict, List, Tuple

import notional
from notional.blocks import Paragraph, TextObject
from notional.query import TextCondition
from notional.types import Date, ExternalFile, Number, RichText, Title
from requests import get

# from notional.text import Annotations

# from more_itertools import grouper


NO_COVER_IMG = "https://via.placeholder.com/150x200?text=No%20Cover"


def export_to_notion(
        all_books: Dict,
        enable_highlight_date: bool,
        enable_book_cover: bool,
        notion_api_auth_token: str,
        notion_database_id: str,
) -> None:
    print("Initiating transfer...\n")

    for title in all_books:
        each_book = all_books[title]
        author = each_book["author"]
        clippings = each_book["highlights"]
        clippings_count = len(clippings)
        (
            formatted_clippings,
            last_date,
        ) = _prepare_aggregated_text_for_one_book(clippings, enable_highlight_date)
        message = _add_book_to_notion(
            title,
            author,
            clippings_count,
            formatted_clippings,
            last_date,
            notion_api_auth_token,
            notion_database_id,
            enable_book_cover,
        )
        if message != "None to add":
            print("✓", message)


def _prepare_aggregated_text_for_one_book(
        clippings: List, enable_highlight_date: bool
) -> Tuple[str, str]:
    # TODO: Special case for books with len(clippings) >= 100 characters. Character limit in a Paragraph block in Notion is 100
    formatted_clippings = []
    for each_clipping in clippings:
        aggregated_text = ""
        text = each_clipping[0]
        page = each_clipping[1]
        location = each_clipping[2]
        date = each_clipping[3]
        is_note = each_clipping[4]
        if is_note == True:
            aggregated_text += "> " + "NOTE: \n"

        aggregated_text += text + "\n* "
        if page != "":
            aggregated_text += "Page: " + page + ", "
        if location != "":
            aggregated_text += "Location: " + location
        if enable_highlight_date and (date != ""):
            aggregated_text += ", Date Added: " + date

        aggregated_text = aggregated_text.strip() + "\n\n"
        formatted_clippings.append(aggregated_text)
        last_date = date
    return formatted_clippings, last_date


def _add_book_to_notion(
        title: str,
        author: str,
        clippings_count: int,
        formatted_clippings: list,
        last_date_string: str,
        notion_api_auth_token: str,
        notion_database_id: str,
        enable_book_cover: bool,
):
    notion = notional.connect(auth=notion_api_auth_token)
    last_date = __get_last_date_from_string(last_date_string)

    # Condition variables
    title_exists = False
    current_clippings_count = 0

    query = (
        notion.databases.query(notion_database_id)
        .filter(property="Title", rich_text=TextCondition(equals=title))
        .limit(1)
    )
    data = query.first()

    if data:
        title_exists = True
        block_id = data.id
        block = notion.pages.retrieve(block_id)
        if block["Highlights"] == None:
            block["Highlights"] = Number[0]
        elif block["Highlights"] == clippings_count:  # if no change in clippings
            title_and_author = str(block["Title"]) + " (" + str(block["Author"]) + ")"
            print(title_and_author)
            print("-" * len(title_and_author))
            return "None to add.\n"

    title_and_author = title + " (" + str(author) + ")"
    print(title_and_author)
    print("-" * len(title_and_author))

    # Add a new book to the database
    if not title_exists:
        new_page = notion.pages.create(
            parent=notion.databases.retrieve(notion_database_id),
            properties={
                "Title": Title[title],
                "Author": RichText[author],
                "Highlights": Number[clippings_count],
                "Last Highlighted": Date[last_date.isoformat()],
                "Last Synced": Date[datetime.now().isoformat()],
            },
            children=[],
        )
        # page_content = _update_book_with_clippings(formatted_clippings)
        page_content = Paragraph["".join(formatted_clippings)]
        notion.blocks.children.append(new_page, page_content)
        block_id = new_page.id
        if enable_book_cover:
            # Fetch a book cover from Google Books if the cover for the page is not set
            if new_page.cover is None:
                result = _get_book_cover_uri(title, author)

            if result is None:
                # Set the page cover to a placeholder image
                cover = ExternalFile[NO_COVER_IMG]
                print(
                    "× Book cover couldn't be found. "
                    "Please replace the placeholder image with the original book cover manually."
                )
            else:
                # Set the page cover to that of the book
                cover = ExternalFile[result]
                print("✓ Added book cover.")

            notion.pages.set(new_page, cover=cover)
    else:
        # update a book that already exists in the database
        page = notion.pages.retrieve(block_id)
        # page_content = _update_book_with_clippings(formatted_clippings)
        page_content = Paragraph["".join(formatted_clippings)]
        notion.blocks.children.append(page, page_content)
        # TODO: Delete existing page children (or figure out how to find changes to be made by comparing it with local json file.)
        current_clippings_count = int(str(page["Highlights"]))
        page["Highlights"] = Number[clippings_count]
        page["Last Highlighted"] = Date[last_date.isoformat()]
        page["Last Synced"] = Date[datetime.now().isoformat()]

    # Logging the changes made
    diff_count = (
        clippings_count - current_clippings_count
        if clippings_count > current_clippings_count
        else clippings_count
    )
    message = str(diff_count) + " notes/highlights added successfully.\n"

    return message


def __get_last_date_from_string(last_date_string: str) -> datetime:
    if not last_date_string:
        return datetime.now()
    try:
        return datetime.strptime(last_date_string, "%A, %d %B %Y %I:%M:%S %p")
    except ValueError:
        # Datetime format is not English, retrying with non AM-PM format
        return datetime.strptime(last_date_string, "%A, %d %B %Y %H:%M:%S")

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
