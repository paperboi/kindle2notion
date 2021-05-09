from notion.collection import NotionDate
from notion.block import TextBlock

from datetime import datetime
from dateparser import parse
import string
import errno
import os
import re
import unicodedata

from utilities import getBookCoverURI, NO_COVER_IMG, ITALIC
from settings import CLIPPINGS_FILE, ENABLE_HIGHLIGHT_DATE, ENABLE_BOOK_COVER, client, cv, allRows


class KindleClippings(object):
    def __init__(self, clippingsFile):
        self.clippings = self._getAllClippings(clippingsFile)

    def _getAllClippings(self, clippingsFile):
        allClippings = open(clippingsFile, 'r', encoding="utf-8-sig").read()
        allClippings = unicodedata.normalize("NFKD", allClippings)
        return self._parseClippings(allClippings)

    def _parseClippings(self, allClippings):
        allClippings = allClippings.split("==========")
        print("Found", len(allClippings), "notes and highlights.\n")

        books = {}
        passedClippingCount = 0

        for eachClipping in allClippings:
            eachClipping = eachClipping.strip().split("\n")

            # Sometimes a null text or a bookmark can be selected as clipping. So check the array size;
            if len(eachClipping) >= 3:
                author = (re.findall(r'\(.*?\)', eachClipping[0]))[-1]
                author = author.removeprefix('(').removesuffix(')')
                title = eachClipping[0].replace(author,'').strip().replace(u'\ufeff', ''). replace(' ()', '')

                # Use-cases that require some additional text-formatting:
                # -------------------------------------------------------
                # 1. If the author's name has a parentheses within it -- ex. "Voltaire (François-Marie Arouet)"
                if '(' in author:
                    author = author + ')'
                    title = title.removesuffix(')')

                # 2. if the author's name is listed in '(Last Name, First Name)' format (only for single authors)  -- ex. "Catch-22 (Heller, Joseph)"
                # TO-DO: Rewrite code to ignore cases where the author's degree is mentioned along with their name -- ex. "Edward M. Hallowell, M.D."" 
                if ', ' in author:
                    lastName, firstName = author.split(', ')
                    author = firstName + " " + lastName

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
                secondLine = eachClipping[1]
                pageOrAndLoc, *optLocAndDate = secondLine.strip().split(' | ')
                dateAdded = ''

                # Extract Added On data from optLocAndDate
                if ENABLE_HIGHLIGHT_DATE:
                    addedOn = optLocAndDate[-1]
                    dateAdded = parse(addedOn[addedOn.find('Added on'):].replace('Added on', '').strip())

               # Extract the actual clipping to this var
                clipping = eachClipping[3]

               # Extract page and location data from pageOrAndLoc
                page = ''
                location = ''

                page = pageOrAndLoc[pageOrAndLoc.find('page'):].replace('page', '').strip()
                location = pageOrAndLoc[pageOrAndLoc.find('location'):].replace('location', '').strip()

                books[title]["highlights"].append((clipping, page, location, dateAdded))

            else:
                # print(eachClipping) # Activate this line for debugging bookmarks or unsupported clippings.
                passedClippingCount += 1

        print("Initiating transfer...\n")

        for title in books:
            book = books[title]
            # print(book)
            author = book["author"]
            # print(author)
            highlightCount = len(book["highlights"])

            # Create single string for all of the notes
            aggregatedText = ""
            d = ""

            for highlight in book["highlights"]:
                c = highlight[0]  # clipping
                p = highlight[1]  # page
                l = highlight[2]  # location
                d = highlight[3]  # date

                aggregatedText += c + "\n("
                if p != '':
                    aggregatedText += ITALIC + "Page: " + p + ITALIC + "\t"

                if l != '':
                    aggregatedText += ITALIC + "Location: " + l + ITALIC + "\t"

                if ENABLE_HIGHLIGHT_DATE and (d is not None and d != ''):
                    aggregatedText += ITALIC + "Date Added: " + \
                        str(d.strftime("%A, %d %B %Y %I:%M:%S %p")) + ITALIC
                aggregatedText = aggregatedText.strip() + ")\n\n"

            message = self.addBookToNotion(title, author, highlightCount, aggregatedText, d)
            if message != "None to add":
                print("✓", message)

        print("\n× Passed", passedClippingCount, "bookmark or unsupported clippings.\n")

    def addBookToNotion(self, title, author, highlightCount, aggregatedText, lastNoteDate):
        titleExists = False

        if allRows != []:
            for eachRow in allRows:
                # to account for the use-case of books with the same name by different authors
                if title == eachRow.title and author == eachRow.author:
                    titleExists = True
                    row = eachRow

                    if row.highlights == None: row.highlights = 0 # to initialize number of highlights as 0
                    elif row.highlights == highlightCount: # if no change in highlights
                        return ("None to add")

        titleAndAuthor = title + " (" + str(author) + ")"
        print(titleAndAuthor)
        print("-" * len(titleAndAuthor))
 
        if not titleExists:
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
                    print("× Book cover couldn't be found. Please replace the placeholder image with the original book cover manually")

        parentPage = client.get_block(row.id)

        # For existing books with new highlights to add
        for allBlocks in parentPage.children:
            allBlocks.remove()
        parentPage.children.add_new(TextBlock, title=aggregatedText)
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
            ch = KindleClippings(CLIPPINGS_FILE)
            print("Transfer complete...\nExiting script...")
    except Exception as e:
        print(str(e))
        print("Exiting script...")
        os.system('pause')

if __name__ == '__main__':
    main()