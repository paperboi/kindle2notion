from notion.client import NotionClient
from notion.collection import NotionDate
from notion.block import QuoteBlock, TextBlock, PageBlock

from datetime import datetime
import string
import os
import unicodedata

from utilities import getBookCoverUri, no_cover_img, BOLD, ITALIC
from settings import CLIPPINGS_FILE, NOTION_TOKEN, NOTION_TABLE_ID, ENABLE_HIGHLIGHT_DATE, ENABLE_BOOK_COVER


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
                secondLine = eachClipping[1] # Second line after ===== marks, for identifying type

                # To-do: Author name can be stated like "Voltaire (francois Marie Arouet)" So author name should be extracted with Regex.
                title_author = eachClipping[0].replace('(', '|').replace(')', '')
                title, *author = title_author.split('|') # supports single authors also
                title = title.strip()

                # Edit book to the books dictionary
                if title not in books:
                    books[title] = { "author": ",".join(author), "highlights": [] }

                # Please regard this hack. This operation can return some pairs like (page and date), (location and date)
                # or 3 values: (page, location, date)
                # We'll get last item for date.
                # Parameter Explanation:
                # 1. pageOrAndLoc: page or and location: page or location & page and location can return
                # 2. optLocAndDate: Optionally Location can return and date can return or only date can return as array

                pageOrAndLoc, *optLocAndDate = secondLine.strip().split('|')
                addedOn = optLocAndDate[-1]
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                page = None
                location = None

                # To-do: These conditions can be reduced to a single Regex

                if '- Your Highlight at location ' in secondLine:
                    location = pageOrAndLoc.replace('- Your Highlight at location ', '').replace(' ', '')

                elif '- Your Note on location ' in secondLine:
                    location = pageOrAndLoc.replace('- Your Note on location ', '').replace(' ', '')

                elif '- Your Highlight on page ' in secondLine and 'location ' in secondLine:
                    page = pageOrAndLoc.replace('- Your Highlight on page ', '').replace(' ', '')
                    location = optLocAndDate[0].replace(' location ', '').replace(' ','')

                elif '- Your Note on page ' in secondLine and 'location ' in secondLine:
                    page = pageOrAndLoc.replace('- Your Note on page ', '').replace(' ', '')
                    location = optLocAndDate[0].replace(' location ', '').replace(' ','')

                elif '- Your Highlight on page ' in secondLine and 'location ' not in secondLine:
                    page = pageOrAndLoc.replace('- Your Highlight on page ', '').replace(' ', '')

                elif '- Your Note on page ' in secondLine and 'location ' not in secondLine:
                    page = pageOrAndLoc.replace('- Your Note on page ', '').replace(' ', '')

                books[title]["highlights"].append((clipping, page, location, dateAdded))

            else:
                # print(eachClipping) # Activate this line for debugging bookmarks or unsupported clippings. 
                passedClippingCount += 1

        print("Initiating tranfer...\n")

        for bookName in books:
            book = books[bookName]
            author = book["author"]
            highlightCount = len(book["highlights"])

            # Create single string for all of the notes
            aggregatedText = ""
            d = ""

            for highlight in book["highlights"]:
                c = highlight[0] # clipping
                p = highlight[1] # page
                l = highlight[2] # location
                d = highlight[3] # date

                aggregatedText += BOLD + c + BOLD + "\n"
                if p != None:
                    aggregatedText += ITALIC + "Page: " + p + ITALIC + "\t"

                if l != None:
                    aggregatedText += ITALIC + "Location: " + l + ITALIC + "\t"

                if ENABLE_HIGHLIGHT_DATE:
                    aggregatedText += ITALIC + "Date Added: " + str(d.strftime("%A, %d %B %Y %I:%M:%S %p")) + ITALIC
                aggregatedText += "\n\n"
                
            message = self.addBookToNotion(bookName, author, highlightCount, d, aggregatedText)
            if message != "None to add":
                print("✓", message)

        print("\n× Passed", passedClippingCount, "bookmark or unsupported clippings.\n")

    def _getClipping(self):
        for i in self.clippings:
            yield i

    def addBookToNotion(self, bookName, author, highlightCount, lastNoteDate, aggregatedText):
        titleExists = False
        newHighlights = True

        global cv, allRows

        if allRows != []:
            for eachRow in allRows:
                if bookName == eachRow.title and author == eachRow.author: # to account for the use-case of books with the same name by different authors
                    titleExists = True
                    row = eachRow

                    if row.highlights == None: row.highlights = 0 # to initialize number of highlights as 0
                    elif row.highlights == highlightCount: # if no change in highlights
                        newHighlights = False
                        return ("None to add")
        
        print(bookName + " (" + author + ")")
        print("-" * len(bookName + " (" + author + ")"))
        if not titleExists:
            row = cv.collection.add_row()
            row.title = bookName
            row.author = author
            row.highlights = 0

            if ENABLE_BOOK_COVER == True: 
                if row.cover == None:
                    result = getBookCoverUri(row.title, row.author)
                if result != None:
                    row.cover = result
                    print("✓ Added book cover")
                else:
                    row.cover = no_cover_img
                    print("× Book cover couldn't be found. Please replace the placeholder image with the original book cover manually")

        parentPage = client.get_block(row.id)


        # For existing books with new highlights to add
        for allBlocks in parentPage.children:
            allBlocks.remove()
        parentPage.children.add_new(TextBlock, title = aggregatedText)
        diffCount = highlightCount - row.highlights
        row.highlights = highlightCount
        row.last_highlighted = NotionDate(lastNoteDate)
        row.last_synced = NotionDate(datetime.now())
        message = str(diffCount) + " notes / highlights added successfully\n"
        return (message)

client = NotionClient(token_v2= NOTION_TOKEN)
cv = client.get_collection_view(NOTION_TABLE_ID)
allRows = cv.collection.get_rows()
print(cv.parent.views)

if len(cv.parent.views) > 0:
    print("Notion page is found. Analyzing clippings file...\n")

ch = KindleClippings(CLIPPINGS_FILE)