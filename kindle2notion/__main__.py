import json

import click
import notional

from kindle2notion.exporting import export_to_notion
from kindle2notion.parsing import parse_raw_clippings_text
from kindle2notion.reading import read_raw_clippings, read_raw_clippings_streamlit


def process_kindle_clippings(
    notion_api_auth_token,
    notion_database_id,
    all_clippings,
    enable_highlight_date,
    enable_book_cover,
):
    # Parse all_clippings file and format the content to be sent tp the Notion DB into all_books
    all_books = parse_raw_clippings_text(all_clippings)
    # Export all the contents in all_books into the Notion DB.
    export_to_notion(
        all_books,
        enable_highlight_date,
        enable_book_cover,
        notion_api_auth_token,
        notion_database_id,
    )
    with open("my_kindle_clippings.json", "w") as out_file:
        json.dump(all_books, out_file, indent=4)
    print("Transfer complete... Exiting script...")


def update_kindle_clippings_streamlit(
    notion_api_auth_token,
    notion_database_id,
    clippings_data,
    enable_highlight_date,
    enable_book_cover,
):
    notion = notional.connect(auth=notion_api_auth_token)
    db = notion.databases.retrieve(notion_database_id)
    if db:
        print("Notion page is found. Analyzing clippings file...")
        # Open the clippings text file and load it into all_clippings
        all_clippings = read_raw_clippings_streamlit(clippings_data)
        process_kindle_clippings(
            notion_api_auth_token,
            notion_database_id,
            all_clippings,
            enable_highlight_date,
            enable_book_cover,
        )
    else:
        print(
            "Notion page not found! Please check whether the Notion database ID is assigned properly."
        )


def update_kindle_clippings(
    notion_api_auth_token,
    notion_database_id,
    clippings_file,
    enable_highlight_date,
    enable_book_cover,
):
    notion = notional.connect(auth=notion_api_auth_token)
    db = notion.databases.retrieve(notion_database_id)
    if db:
        print("Notion page is found. Analyzing clippings file...")
        # Open the clippings text file and load it into all_clippings
        all_clippings = read_raw_clippings(clippings_file)
        process_kindle_clippings(
            notion_api_auth_token,
            notion_database_id,
            all_clippings,
            enable_highlight_date,
            enable_book_cover,
        )
    else:
        print(
            "Notion page not found! Please check whether the Notion database ID is assigned properly."
        )


@click.command()
@click.argument("notion_api_auth_token")
@click.argument("notion_database_id")
@click.argument("clippings_file")
@click.option(
    "--enable_highlight_date",
    default=True,
    help='Set to False if you don\'t want to see the "Date Added" information in Notion.',
)
@click.option(
    "--enable_book_cover",
    default=True,
    help="Set to False if you don't want to store the book cover in Notion.",
)
def main(
    notion_api_auth_token,
    notion_database_id,
    clippings_file,
    enable_highlight_date,
    enable_book_cover,
):
    update_kindle_clippings(
        notion_api_auth_token,
        notion_database_id,
        clippings_file,
        enable_highlight_date,
        enable_book_cover,
    )


if __name__ == "__main__":
    main()
