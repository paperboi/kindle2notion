import sys

from decouple import config
from notion.client import NotionClient

# Store these values in an .env file in this directory (See "/.env.example").
CLIPPINGS_FILE = config('CLIPPINGS_FILE')
TEST_CLIPPINGS_FILE = config('TEST_CLIPPINGS_FILE')
NOTION_TOKEN = config('NOTION_TOKEN')
NOTION_TABLE_ID = config('NOTION_TABLE_ID')
ENABLE_HIGHLIGHT_DATE = config('ENABLE_HIGHLIGHT_DATE') == "True"  # If not returns False
ENABLE_BOOK_COVER = config('ENABLE_BOOK_COVER') == "True"

client = NotionClient(token_v2=NOTION_TOKEN)
cv = client.get_collection_view(NOTION_TABLE_ID)
all_rows = cv.collection.get_rows()

if not sys.version_info >= (3, 5):
    print("Please update your Python version via the 'python -m pip install –upgrade pip' command.")
