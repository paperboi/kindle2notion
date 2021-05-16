import os

from kindle2notion.exporting import export_to_notion
from kindle2notion.parsing import parse_clippings
from kindle2notion.reading import read_raw_clippings
from kindle2notion.settings import CLIPPINGS_FILE, NOTION_COLLECTION_VIEW


def main():
    try:
        if len(NOTION_COLLECTION_VIEW.parent.views) > 0:
            print('Notion page is found. Analyzing clippings file...\n')
            all_clippings = read_raw_clippings(CLIPPINGS_FILE)
            books = parse_clippings(all_clippings)
            export_to_notion(books)
            print('Transfer complete...\nExiting script...')
    except Exception as e:
        print(str(e))
        print('Exiting script...')
        os.system('pause')


if __name__ == '__main__':
    main()
