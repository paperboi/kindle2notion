import sys

from decouple import config
# Store these values in an .env file in this directory (See '/.env.example').
from notion.client import NotionClient

CLIPPINGS_FILE = config('CLIPPINGS_FILE')
TEST_CLIPPINGS_FILE = config('TEST_CLIPPINGS_FILE')
NOTION_TOKEN = config('NOTION_TOKEN')
NOTION_TABLE_ID = config('NOTION_TABLE_ID')
ENABLE_HIGHLIGHT_DATE = config('ENABLE_HIGHLIGHT_DATE') == 'True'  # If not returns False
ENABLE_BOOK_COVER = config('ENABLE_BOOK_COVER') == 'True'

NOTION_CLIENT = NotionClient(token_v2=NOTION_TOKEN)
NOTION_COLLECTION_VIEW = NOTION_CLIENT.get_collection_view(NOTION_TABLE_ID)
NOTION_COLLECTION_VIEW_ROWS = NOTION_COLLECTION_VIEW.collection.get_rows()

if not sys.version_info >= (3, 5):
    print('Please update your Python version via the "python -m pip install –upgrade pip" command.')
