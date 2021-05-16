from datetime import datetime

from notion.block import TextBlock
from notion.collection import NotionDate

from settings import ENABLE_HIGHLIGHT_DATE, ENABLE_BOOK_COVER, client, notion_collection_view, \
    notion_collection_view_rows
from utilities import getBookCoverURI, NO_COVER_IMG, ITALIC


def export_to_notion(books):
    print('Initiating transfer...\n')
    for title in books:
        book = books[title]
        author = book['author']
        highlights = book['highlights']
        highlight_count = len(highlights)
        aggregated_text_from_highlights, last_date = prepare_aggregated_text_for_one_book(highlights)

        message = add_book_to_notion(title, author, highlight_count, aggregated_text_from_highlights, last_date)
        if message != 'None to add':
            print('✓', message)


def prepare_aggregated_text_for_one_book(highlights):
    aggregated_text = ''
    for highlight in highlights:
        text = highlight[0]
        page = highlight[1]
        location = highlight[2]
        date = highlight[3]

        aggregated_text += text + '\n('
        if page != '':
            aggregated_text += ITALIC + 'Page: ' + page + ITALIC + '\t'
        if location != '':
            aggregated_text += ITALIC + 'Location: ' + location + ITALIC + '\t'
        if ENABLE_HIGHLIGHT_DATE and (date is not None and date != ''):
            aggregated_text += ITALIC + 'Date Added: ' + str(date.strftime('%A, %d %B %Y %I:%M:%S %p')) + ITALIC

        aggregated_text = aggregated_text.strip() + ')\n\n'
    last_date = date
    return aggregated_text, last_date


def add_book_to_notion(title, author, highlightCount, aggregatedText, lastNoteDate):
    title_exists = False

    if notion_collection_view_rows != []:
        for each_row in notion_collection_view_rows:
            # to account for the use-case of books with the same name by different authors
            if title == each_row.title and author == each_row.author:
                title_exists = True
                row = each_row

                if row.highlights == None:
                    row.highlights = 0  # to initialize number of highlights as 0
                elif row.highlights == highlightCount:  # if no change in highlights
                    return ('None to add')

    title_and_author = title + ' (' + str(author) + ')'
    print(title_and_author)
    print('-' * len(title_and_author))

    if not title_exists:
        row = notion_collection_view.collection.add_row()
        row.title = title
        row.author = author
        row.highlights = 0

        if ENABLE_BOOK_COVER:
            if row.cover == None:
                result = getBookCoverURI(row.title, row.author)
            if result != None:
                row.cover = result
                print('✓ Added book cover')
            else:
                row.cover = NO_COVER_IMG
                print(
                    '× Book cover couldn\'t be found. Please replace the placeholder image with the original book cover manually')

    parent_page = client.get_block(row.id)

    # For existing books with new highlights to add
    for all_blocks in parent_page.children:
        all_blocks.remove()
    parent_page.children.add_new(TextBlock, title=aggregatedText)
    diffCount = highlightCount - row.highlights
    row.highlights = highlightCount
    row.last_highlighted = NotionDate(lastNoteDate)
    row.last_synced = NotionDate(datetime.now())
    message = str(diffCount) + ' notes / highlights added successfully\n'
    return (message)
