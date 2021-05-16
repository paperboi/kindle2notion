import os
import re
import unicodedata
from datetime import datetime

from dateparser import parse
from notion.block import TextBlock
from notion.collection import NotionDate

from settings import CLIPPINGS_FILE, ENABLE_HIGHLIGHT_DATE, ENABLE_BOOK_COVER, client, cv, all_rows
from utilities import getBookCoverURI, NO_COVER_IMG, ITALIC


def get_all_clippings(clippings_file):
    all_clippings = open(clippings_file, 'r', encoding="utf-8-sig").read()
    all_clippings = unicodedata.normalize("NFKD", all_clippings)
    return all_clippings


def parse_clippings(all_clippings):
    all_clippings = all_clippings.split("==========")
    print("Found", len(all_clippings), "notes and highlights.\n")

    books = {}
    passed_clipping_count = 0

    for each_clipping in all_clippings:
        each_clipping = each_clipping.strip().split("\n")

        # Sometimes a null text or a bookmark can be selected as clipping. So check the array size;
        if len(each_clipping) >= 3:
            author = (re.findall(r'\(.*?\)', each_clipping[0]))[-1]
            author = author.removeprefix('(').removesuffix(')')
            title = each_clipping[0].replace(author, '').strip().replace(u'\ufeff', '').replace(' ()', '')

            # Use-cases that require some additional text-formatting:
            # -------------------------------------------------------
            # 1. If the author's name has a parentheses within it -- ex. "Voltaire (François-Marie Arouet)"
            if '(' in author:
                author = author + ')'
                title = title.removesuffix(')')

            # 2. if the author's name is listed in '(Last Name, First Name)' format (only for single authors)  -- ex. "Catch-22 (Heller, Joseph)"
            # TO-DO: Rewrite code to ignore cases where the author's degree is mentioned along with their name -- ex. "Edward M. Hallowell, M.D.""
            if ', ' in author:
                last_name, first_name = author.split(', ')
                author = first_name + " " + last_name

            # 3. If title of the book is listed as 'Placeholder, The' -- ex. "Mysterious Disappearance of Leon (I Mean Noel), The"
            if ', The' in title:
                title = 'The ' + title.replace(', The', '')

            # Edit book to the books dictionary
            if title not in books:
                books[title] = {"author": author, "highlights": []}

            # Please regard this hack. This operation can return some pairs like (page and date), (location and date)
            # or 3 values: (page, location, date)
            # We'll get last item for date.
            # Parameter Explanation:
            # 1. pageOrAndLoc: page or and location: page or location & page and location can return
            # 2. optLocAndDate: Optionally Location can return and date can return or only date can return as array

            # Second line after ===== marks, for identifying type
            second_line = each_clipping[1]
            pageOrAndLoc, *optLocAndDate = second_line.strip().split(' | ')
            date_added = ''

            # Extract Added On data from optLocAndDate
            if ENABLE_HIGHLIGHT_DATE:
                addedOn = optLocAndDate[-1]
                date_added = parse(addedOn[addedOn.find('Added on'):].replace('Added on', '').strip())

            # Extract the actual clipping to this var
            clipping = each_clipping[3]

            # Extract page and location data from pageOrAndLoc
            page = pageOrAndLoc[pageOrAndLoc.find('page'):].replace('page', '').strip()
            location = pageOrAndLoc[pageOrAndLoc.find('location'):].replace('location', '').strip()

            books[title]["highlights"].append((clipping, page, location, date_added))

        else:
            # print(eachClipping) # Activate this line for debugging bookmarks or unsupported clippings.
            passed_clipping_count += 1

    return books, passed_clipping_count


def transfer_to_notion(books, passed_clipping_count):
    print("Initiating transfer...\n")
    for title in books:
        aggregated_text, author, d, highlight_count = prepare_notion_information_for_one_book(books, title)

        message = add_book_to_notion(title, author, highlight_count, aggregated_text, d)
        if message != "None to add":
            print("✓", message)
    print("\n× Passed", passed_clipping_count, "bookmark or unsupported clippings.\n")


def prepare_notion_information_for_one_book(books, title):
    book = books[title]
    # print(book)
    author = book["author"]
    # print(author)
    highlight_count = len(book["highlights"])
    # Create single string for all of the notes
    aggregated_text = ""
    d = ""
    for highlight in book["highlights"]:
        c = highlight[0]  # clipping
        p = highlight[1]  # page
        l = highlight[2]  # location
        d = highlight[3]  # date

        aggregated_text += c + "\n("
        if p != '':
            aggregated_text += ITALIC + "Page: " + p + ITALIC + "\t"

        if l != '':
            aggregated_text += ITALIC + "Location: " + l + ITALIC + "\t"

        if ENABLE_HIGHLIGHT_DATE and (d is not None and d != ''):
            aggregated_text += ITALIC + "Date Added: " + \
                               str(d.strftime("%A, %d %B %Y %I:%M:%S %p")) + ITALIC
        aggregated_text = aggregated_text.strip() + ")\n\n"
    return aggregated_text, author, d, highlight_count


def add_book_to_notion(self, title, author, highlightCount, aggregatedText, lastNoteDate):
    title_exists = False

    if all_rows != []:
        for each_row in all_rows:
            # to account for the use-case of books with the same name by different authors
            if title == each_row.title and author == each_row.author:
                title_exists = True
                row = each_row

                if row.highlights == None:
                    row.highlights = 0  # to initialize number of highlights as 0
                elif row.highlights == highlightCount:  # if no change in highlights
                    return ("None to add")

    title_and_author = title + " (" + str(author) + ")"
    print(title_and_author)
    print("-" * len(title_and_author))

    if not title_exists:
        row = cv.collection.add_row()
        row.title = title
        row.author = author
        row.highlights = 0

        if ENABLE_BOOK_COVER:
            if row.cover == None:
                result = getBookCoverURI(row.title, row.author)
            if result != None:
                row.cover = result
                print("✓ Added book cover")
            else:
                row.cover = NO_COVER_IMG
                print(
                    "× Book cover couldn't be found. Please replace the placeholder image with the original book cover manually")

    parent_page = client.get_block(row.id)

    # For existing books with new highlights to add
    for all_blocks in parent_page.children:
        all_blocks.remove()
    parent_page.children.add_new(TextBlock, title=aggregatedText)
    diffCount = highlightCount - row.highlights
    row.highlights = highlightCount
    row.last_highlighted = NotionDate(lastNoteDate)
    row.last_synced = NotionDate(datetime.now())
    message = str(diffCount) + " notes / highlights added successfully\n"
    return (message)


def main():
    try:
        if len(cv.parent.views) > 0:
            print("Notion page is found. Analyzing clippings file...\n")
            all_clippings = get_all_clippings(CLIPPINGS_FILE)
            books, passed_clipping_count = parse_clippings(all_clippings)
            transfer_to_notion(books, passed_clipping_count)
            print("Transfer complete...\nExiting script...")
    except Exception as e:
        print(str(e))
        print("Exiting script...")
        os.system('pause')


if __name__ == '__main__':
    main()
