import os
from typing import Optional

import click
import notional

from kindle2notion.exporting import export_to_notion
from kindle2notion.parsing import parse_raw_clippings_text
from kindle2notion.reading import read_raw_clippings
from kindle2notion.package_logger import logger


@click.command()
@click.argument("clippings_file")
@click.option(
    "--enable_location",
    default=True,
    help='Set to False if you don\'t want to see the "Location" and "Page" information in Notion.',
)
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
@click.option(
    "--separate_blocks",
    default=False,
    help="Set to True to separate each clipping into a separate quote block. Enabling this option significantly decreases upload speed.",
)
@click.option(
    "--kindle_root",
    type=str,
    help="Path to kindle root when connected. This will help in fetching headings from the respective book when adding to notion",
    default=None,
)
def main(
    clippings_file,
    enable_location,
    enable_highlight_date,
    enable_book_cover,
    separate_blocks,
    kindle_root: Optional[str],
):
    notion_api_auth_token = os.environ.get("NOTION_AUTH_TOKEN", None)
    notion_database_id = os.environ.get("NOTION_DBREF", None)
    if notion_api_auth_token is None:
        logger.error("please export the env var: NOTION_AUTH_TOKEN")
        return
    if notion_database_id is None:
        logger.error("please export the following env var: NOTION_DBREF")
        return
    notion = notional.connect(auth=notion_api_auth_token)
    db = notion.databases.retrieve(notion_database_id)

    if db:
        logger.info("Notion page is found. Analyzing clippings file...")
        # Open the clippings text file and load it into all_clippings
        all_clippings = read_raw_clippings(clippings_file)

        # Parse all_clippings file and format the content to be sent tp the Notion DB into all_books
        all_books = parse_raw_clippings_text(all_clippings)
        # Export all the contents in all_books into the Notion DB.

        # ######### FIXME TESTING
        # my_book = "Thinking in Bets"
        # all_books = {my_book: all_books[my_book]}
        # ###################
        export_to_notion(
            all_books,
            enable_location,
            enable_highlight_date,
            enable_book_cover,
            separate_blocks,
            notion_api_auth_token,
            notion_database_id,
            kindle_root=kindle_root,
        )

        # with open("my_kindle_clippings.json", "w") as out_file:
        #     json.dump(all_books, out_file, indent=4)

        logger.info("Transfer complete... Exiting script...")
    else:
        logger.error(
            "Notion page not found! Please check whether the Notion database ID is assigned properly."
        )


if __name__ == "__main__":
    main()
