import os
from decouple import config

# Store these values in an .env file in this directory
CLIPPINGS_FILE = config('CLIPPINGS_FILE')
NOTION_TOKEN = config('NOTION_TOKEN')
NOTION_PAGE_ID = config('NOTION_PAGE_ID')