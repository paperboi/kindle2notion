from datetime import datetime
from operator import contains
from typing import Dict, List, Tuple

import notional
from notional.query import TextCondition
from notional import blocks, types

from requests import get

NO_COVER_IMG = "https://via.placeholder.com/150x200?text=No%20Cover"
ITALIC = "*"
BOLD = "**"    


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
        highlights = each_book["highlights"]
        highlight_count = len(highlights)
        (
            aggregated_text_from_highlights,
            last_date,
        ) = _prepare_aggregated_text_for_one_book(highlights, enable_highlight_date)
        message = _add_book_to_notion(
            title,
            author,
            highlight_count,
            aggregated_text_from_highlights,
            last_date,
            notion_api_auth_token,
            notion_database_id,
            enable_book_cover,
        )
        if message != "None to add":
            print("✓", message)


def _prepare_aggregated_text_for_one_book(
    highlights: List,
    enable_highlight_date: bool
) -> Tuple[str, str]:
    aggregated_text = ""
    for highlight in highlights:
        text = highlight[0]
        page = highlight[1]
        location = highlight[2]
        date = highlight[3]
        isNote = highlight[4]
        if isNote == True:
            aggregated_text += BOLD + "Note: " + BOLD

        aggregated_text += text + "\n("
        if page != "":
            aggregated_text += ITALIC + "Page: " + page + ITALIC + "  "
        if location != "":
            aggregated_text += ITALIC + "Location: " + location + ITALIC + "  "
        if enable_highlight_date and (date != ""):
            aggregated_text += ITALIC + "Date Added: " + date + ITALIC

        aggregated_text = aggregated_text.strip() + ")\n\n"
        last_date = date
    return aggregated_text, last_date


def _add_book_to_notion(
    title: str,
    author: str,
    highlight_count: int,
    aggregated_text: str,
    last_date: str,
    notion_api_auth_token: str,
    notion_database_id: str,
    enable_book_cover: bool
    ):
    notion = notional.connect(auth=notion_api_auth_token)
    last_date = datetime.strptime(last_date, "%A, %d %B %Y %I:%M:%S %p")

    title_exists = False
    query = notion.databases.query(notion_database_id).filter(property="Title", rich_text=TextCondition(equals=title)).limit(1)
    data = query.first()

    if data:
        title_exists = True
        block_id = data.id
        block = notion.pages.retrieve(block_id)
        if block["Highlights"] == None:
            block["Highlights"] = types.Number[0]
        elif block["Highlights"] == highlight_count: # if no change in highlights
            title_and_author = str(block["Title"]) + " (" + str(block["Author"]) + ")"
            print(title_and_author)
            print("-" * len(title_and_author))
            return "None to add.\n"

    title_and_author = title + " (" + str(author) + ")"
    print(title_and_author)
    print("-" * len(title_and_author))

    if not title_exists:
        new_page = notion.pages.create(
            parent=notion.databases.retrieve(notion_database_id),
            properties={
                "Title": types.Title[title],
                "Author": types.RichText[author],
                "Highlights": types.Number[highlight_count],
                "Last Highlighted": types.Date[last_date.isoformat()],
                "Last Synced": types.Date[datetime.now().isoformat()]
            },
            children=[blocks.Paragraph[aggregated_text]],
        )
        block_id = new_page.id
        if enable_book_cover:
            if new_page.cover is None:
                result = _get_book_cover_uri(title, author)
            if result is not None:
                cover = types.ExternalFile[result]
                print("✓ Added book cover.")
            else:
                cover = types.ExternalFile[NO_COVER_IMG]
                print(
                    "× Book cover couldn't be found. "
                    "Please replace the placeholder image with the original book cover manually."
                    )
            notion.pages.set(new_page, cover=cover)

    block = notion.pages.retrieve(block_id)
    current_highlight_count = int(str(block["Highlights"]))
    diff_count = highlight_count - current_highlight_count if highlight_count > current_highlight_count else highlight_count

    block["Highlights"] = types.Number[highlight_count]
    block["Last Highlighted"] = types.Date[last_date]
    block["Last Synced"] = types.Date[datetime.now()]

    message = str(diff_count) + " notes/highlights added successfully.\n"
    return message


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