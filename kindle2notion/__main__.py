import click
from notion.client import NotionClient

from kindle2notion.exporting import export_to_notion
from kindle2notion.parsing import parse_raw_clippings_text
from kindle2notion.reading import read_raw_clippings


@click.command()
@click.argument('notion_token')
@click.argument('notion_table_id')
@click.option('--clippings_file_path', default='/Volumes/Kindle/documents/My Clippings.txt',
              help='Define the absolute path to your Kindle clippings file.')
@click.option('--enable_highlight_date', default=True,
              help='Set to False if you don\'t want to see the "Date Added" information in Notion.')
@click.option('--enable_book_cover', default=True,
              help='Set to False if you don\'t want to store the book cover in Notion.')
def main(notion_token, notion_table_id, clippings_file_path, enable_highlight_date, enable_book_cover):

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
