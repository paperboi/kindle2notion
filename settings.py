import os
from decouple import config

# Store these values in an .env file in this directory (See "/.env.example").
CLIPPINGS_FILE = config('CLIPPINGS_FILE')
NOTION_TOKEN = config('NOTION_TOKEN')
NOTION_TABLE_ID = config('NOTION_TABLE_ID')