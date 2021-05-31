from datetime import datetime
from typing import Dict, List, Tuple

from dateparser import parse
from notion.block import TextBlock
from notion.client import NotionClient
from notion.collection import NotionDate
from requests import get

NO_COVER_IMG = 'https://via.placeholder.com/150x200?text=No%20Cover'
ITALIC = '*'


# TODO: Refactor this module


def export_to_notion(books: Dict, enable_highlight_date: bool, enable_book_cover: bool, notion_token: str,
                     notion_table_id: str) -> None:
    print('Initiating transfer...\n')

    for title in books:
        book = books[title]
        author = book['author']
        highlights = book['highlights']
        highlight_count = len(highlights)
        aggregated_text_from_highlights, last_date = _prepare_aggregated_text_for_one_book(highlights, enable_highlight_date)
        message = _add_book_to_notion(title, author, highlight_count, aggregated_text_from_highlights, last_date,
                                        notion_token, notion_table_id, enable_book_cover)
        if message != 'None to add':
            print('✓', message)


def _prepare_aggregated_text_for_one_book(highlights: List, enable_highlight_date: bool) -> Tuple[str, str]:
    aggregated_text = ''
    for highlight in highlights:
        text = highlight[0]
        page = highlight[1]
        location = highlight[2]
        date = highlight[3]

        aggregated_text += text + '\n('
        if page != '':
            aggregated_text += ITALIC + 'Page: ' + page + ITALIC + '  '
        if location != '':
            aggregated_text += ITALIC + 'Location: ' + location + ITALIC + '  '
        if enable_highlight_date and (date != ''):
            aggregated_text += ITALIC + 'Date Added: ' + date + ITALIC

        aggregated_text = aggregated_text.strip() + ')\n\n'
    last_date = date
    return aggregated_text, last_date


def _add_book_to_notion(title: str, author: str, highlight_count: int, aggregated_text: str, last_date: str,
                        notion_token: str, notion_table_id: str, enable_book_cover: bool) -> str:
    notion_client = NotionClient(token_v2=notion_token)
    notion_collection_view = notion_client.get_collection_view(notion_table_id)
    notion_collection_view_rows = notion_collection_view.collection.get_rows()

    title_exists = False
    if notion_collection_view_rows:
        for row in notion_collection_view_rows:
            if title == row.title and author == row.author:
                title_exists = True
                row = row

                if row.highlights is None:
                    row.highlights = 0  # to initialize number of highlights as 0
                elif row.highlights == highlight_count:  # if no change in highlights
                    return 'None to add'

    title_and_author = title + ' (' + str(author) + ')'
    print(title_and_author)
    print('-' * len(title_and_author))

    if not title_exists:
        row = notion_collection_view.collection.add_row()
        row.title = title
        row.author = author
        row.highlights = 0

        if enable_book_cover:
            if row.cover is None:
                result = _get_book_cover_uri(row.title, row.author)
            if result is not None:
                row.cover = result
                print('✓ Added book cover')
            else:
                row.cover = NO_COVER_IMG
                print('× Book cover couldn\'t be found. '
                      'Please replace the placeholder image with the original book cover manually.')

    parent_page = notion_client.get_block(row.id)

    # For existing books with new highlights to add
    for all_blocks in parent_page.children:
        all_blocks.remove()
    parent_page.children.add_new(TextBlock, title=aggregated_text)
    diff_count = highlight_count - row.highlights
    row.highlights = highlight_count
    row.last_highlighted = NotionDate(parse(last_date))
    row.last_synced = NotionDate(datetime.now())
    message = str(diff_count) + ' notes / highlights added successfully\n'
    return message


def _get_book_cover_uri(title: str, author: str):
    req_uri = 'https://www.googleapis.com/books/v1/volumes?q='

    if title is None:
        return
    req_uri += 'intitle:' + title

    if author is not None:
        req_uri += '+inauthor:' + author

    response = get(req_uri).json().get('items', [])
    if len(response) > 0:
        return (
            response[0]
            .get('volumeInfo', {})
            .get('imageLinks', {})
            .get('thumbnail')
            .replace(
                'http://',
                'https://',
                count=1)
            )

    return
