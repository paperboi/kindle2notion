from datetime import datetime
from typing import Dict, List, Tuple

from notion.block import TextBlock
from notion.collection import NotionDate
from requests import get

from kindle2notion.settings import ENABLE_HIGHLIGHT_DATE, ENABLE_BOOK_COVER, NOTION_CLIENT, NOTION_COLLECTION_VIEW, \
    NOTION_COLLECTION_VIEW_ROWS, NO_COVER_IMG, ITALIC


def export_to_notion(books: Dict) -> None:
    print('Initiating transfer...\n')

    for title in books:
        book = books[title]
        author = book['author']
        highlights = book['highlights']
        highlight_count = len(highlights)
        aggregated_text_from_highlights, last_date = _prepare_aggregated_text_for_one_book(highlights)

        message = _add_book_to_notion(title, author, highlight_count, aggregated_text_from_highlights, last_date)
        if message != 'None to add':
            print('✓', message)


def _prepare_aggregated_text_for_one_book(highlights: List) -> Tuple[str, str]:
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
        if ENABLE_HIGHLIGHT_DATE and (date is not None and date != ''):
            aggregated_text += ITALIC + 'Date Added: ' + str(date.strftime('%A, %d %B %Y %I:%M:%S %p')) + ITALIC

        aggregated_text = aggregated_text.strip() + ')\n\n'
    last_date = date
    return aggregated_text, last_date


def _add_book_to_notion(title: str, author: str, highlight_count: int, aggregated_text: str, last_date: str) -> str:
    title_exists = False

    if NOTION_COLLECTION_VIEW_ROWS:
        for each_row in NOTION_COLLECTION_VIEW_ROWS:
            if title == each_row.title and author == each_row.author:
                title_exists = True
                row = each_row

                if row.highlights == None:
                    row.highlights = 0  # to initialize number of highlights as 0
                elif row.highlights == highlight_count:  # if no change in highlights
                    return 'None to add'

    title_and_author = title + ' (' + str(author) + ')'
    print(title_and_author)
    print('-' * len(title_and_author))

    if not title_exists:
        row = NOTION_COLLECTION_VIEW.collection.add_row()
        row.title = title
        row.author = author
        row.highlights = 0

        if ENABLE_BOOK_COVER:
            if row.cover == None:
                result = _get_book_cover_uri(row.title, row.author)
            if result != None:
                row.cover = result
                print('✓ Added book cover')
            else:
                row.cover = NO_COVER_IMG
                print('× Book cover couldn\'t be found. '
                      'Please replace the placeholder image with the original book cover manually')

    parent_page = NOTION_CLIENT.get_block(row.id)

    # For existing books with new highlights to add
    for all_blocks in parent_page.children:
        all_blocks.remove()
    parent_page.children.add_new(TextBlock, title=aggregated_text)
    diff_count = highlight_count - row.highlights
    row.highlights = highlight_count
    row.last_highlighted = NotionDate(last_date)
    row.last_synced = NotionDate(datetime.now())
    message = str(diff_count) + ' notes / highlights added successfully\n'
    return message


def _get_book_cover_uri(title: str, author: str):
    req_uri = 'https://www.googleapis.com/books/v1/volumes?q='

    if title == None: return
    req_uri += 'intitle:' + title

    if author != None:
        req_uri += '+inauthor:' + author

    response = get(req_uri).json().get('items', [])
    if len(response) > 0:
        return response[0].get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail')

    return
