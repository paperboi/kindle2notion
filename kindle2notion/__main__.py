from decouple import config
from notion.client import NotionClient

from kindle2notion.exporting import export_to_notion
from kindle2notion.parsing import parse_raw_clippings_text
from kindle2notion.reading import read_raw_clippings


def main():
    clippings_file_path = config('CLIPPINGS_FILE')
    enable_highlight_date = config('ENABLE_HIGHLIGHT_DATE')
    enable_book_cover = config('ENABLE_BOOK_COVER')

    notion_token = config('NOTION_TOKEN')
    notion_table_id = config('NOTION_TABLE_ID')
    notion_client = NotionClient(token_v2=notion_token)
    notion_collection_view = notion_client.get_collection_view(notion_table_id)

    if len(notion_collection_view.parent.views) > 0:
        print('Notion page is found. Analyzing clippings file...')
        all_clippings = read_raw_clippings(clippings_file_path)
        books = parse_raw_clippings_text(all_clippings)
        export_to_notion(books, enable_highlight_date, enable_book_cover, notion_token, notion_table_id)
        print('Transfer complete... Exiting script...')


if __name__ == '__main__':
    main()
