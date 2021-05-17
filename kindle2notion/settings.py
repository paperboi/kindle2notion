import sys

from decouple import config
from notion.client import NotionClient

from pathlib import Path

# Store these values in an .env file in this directory (See '/.env.example').
CLIPPINGS_FILE = config('CLIPPINGS_FILE')
TEST_CLIPPINGS_FILE = Path(__file__).parents[1].absolute()/'tests/test_data/Test Clippings.txt'
NOTION_TOKEN = config('NOTION_TOKEN')
NOTION_TABLE_ID = config('NOTION_TABLE_ID')
ENABLE_HIGHLIGHT_DATE = config('ENABLE_HIGHLIGHT_DATE') == 'True'  # If not returns False
ENABLE_BOOK_COVER = config('ENABLE_BOOK_COVER') == 'True'

NOTION_CLIENT = NotionClient(token_v2=NOTION_TOKEN)
NOTION_COLLECTION_VIEW = NOTION_CLIENT.get_collection_view(NOTION_TABLE_ID)
NOTION_COLLECTION_VIEW_ROWS = NOTION_COLLECTION_VIEW.collection.get_rows()

NO_COVER_IMG = 'https://via.placeholder.com/150x200?text=No%20Cover'
ITALIC = '*'

if not sys.version_info >= (3, 5):
    print('Please update your Python version via the "python -m pip install –upgrade pip" command.')
