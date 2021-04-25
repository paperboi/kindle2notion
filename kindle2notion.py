from notion.client import NotionClient
from notion.collection import NotionDate
from notion.block import QuoteBlock, TextBlock, PageBlock

from datetime import datetime
import string
import os
import unicodedata
from settings import CLIPPINGS_FILE, NOTION_TOKEN, NOTION_TABLE_ID
from utilities import getBookCoverUri, no_cover_img

class KindleClippings(object):
    def __init__(self, clippingsFile):
        self.clippings = self._getAllClippings(clippingsFile)

    def _getAllClippings(self, clippingsFile):
        allClippings = open(clippingsFile, 'r', encoding="utf-8-sig").read()
        allClippings = unicodedata.normalize("NFKD", allClippings)
        return self._parseClippings(allClippings)

    def _parseClippings(self, allClippings):
        allClippings = allClippings.split("==========")
        print("Found", len(allClippings), "notes and highlights.", newLine)

        # books = {"title": {"author": author, "highlights": [(clipping (0), page (1), location (2), dateAdded (3))]}}
        books = {}
        passedClippingCount = 0

        for eachClipping in allClippings:
            eachClipping = eachClipping.strip().split("\n")
     
            # Sometimes a null text or a bookmark can be selected as clipping. So check the array size;
            if len(eachClipping) >= 3:
                secondLine = eachClipping[1] # Second line after = marks, for identifying type

                # TODO: Author name can be stated like "Voltaire (francois Marie Arouet)" So author name should be extracted with Regex.
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
            
                # TODO: This conditions can be reduced to a single Regex
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

        bookCount = len(books)
        print("Initiating tranfer for", bookCount, "books.", newLine)
        bookCounter = 1
        for bookName in books:
            book = books[bookName]
            author = book["author"]
            highlights = book["highlights"]
            highlightCount = len(highlights)
            # Create single string for all of the notes
            aggregatedText = ""
            d = ""
            for highlight in highlights:
                c = highlight[0] # clipping
                p = highlight[1] # page
                l = highlight[2] # location
                d = highlight[3] # date
                aggregatedText += bold + c + bold + newLine
                if p != None:
                    aggregatedText += italic + "Page: " + p + italic + tab
                if l != None:
                    aggregatedText += italic + "Location: " + l + italic + tab
                if ENABLE_HIGHLIGHT_DATE:
                    aggregatedText += italic + "Date Added: " + str(d.strftime("%A, %d %B %Y %I:%M:%S %p")) + italic
                aggregatedText += newLine * 2
                
            self.addBookToNotion(bookName, author, highlightCount, d, aggregatedText)
            print("✓ Book", bookCounter, "/", bookCount, "\t", highlightCount, "\tnotes / highlights has added successfully, from:", bookName, "("+author+")")
            bookCounter += 1

        print(newLine + "× Passed", passedClippingCount, "bookmark or unsupported clippings.", newLine)

    def _getClipping(self):
        for i in self.clippings:
            yield i
    
    def _lenClippings(self):
        return len(self.clippings)
  
    def addBookToNotion(self, bookName, author, highlightCount, lastNoteDate, aggregatedText):
        titleExists = False
        global cv, allRows
        if allRows != []:
            for eachRow in allRows:
                if bookName == eachRow.title:
                    titleExists = True
                    row = eachRow
                    if row.highlights == None: row.highlights = 0
                    # TODO Add some options to clear/keep previous highlights.

        if not titleExists:
            row = cv.collection.add_row()
            row.title = bookName
            row.highlights = 0
        row.author = author # User can delete author, so update it again
        # TODO: If there is two books with same title but with different authors these can be merged.
        parentPage = client.get_block(row.id)
        allClippings = parentPage.children.filter(QuoteBlock)
        for eachClip in allClippings:
            if lastClip['Clipping'].strip() == eachClip.title:
                    clipExists = True
        if clipExists == False:
            if lastClip['Location'] != None:
                if lastClip['Page'] != None:
                    parentPage.children.add_new(
                        TextBlock,
                        title = "Page: " + lastClip['Page'] + "\tLocation: " + lastClip['Location'] + "\tDate Added: " +  str(lastClip['Date Added'].strftime("%A, %d %B %Y %I:%M:%S %p"))
                    )
                else:
                    parentPage.children.add_new(
                        TextBlock,
                        title = "Location: " + lastClip['Location'] + "\tDate Added: " +  str(lastClip['Date Added'].strftime("%A, %d %B %Y %I:%M:%S %p"))
                    )
            else:
                parentPage.children.add_new(
                    TextBlock,
                    title = "Page: " + lastClip['Page'] + "\tDate Added: " +  str(lastClip['Date Added'].strftime("%A, %d %B %Y %I:%M:%S %p"))
                )
            parentPage.children.add_new(
                QuoteBlock,
                title = lastClip['Clipping']
            )
            row.highlights +=1
            row.last_highlighted = NotionDate(lastClip['Date Added'])
            row.last_synced = NotionDate(datetime.now())

def generateBookCovers(cv):
    all_rows = cv.collection.get_rows()
    coverCount = len(all_rows)
    coverCounter = 1
    print("Generating book covers...")
    for record in all_rows: 
        if record.cover == None:
            result = getBookCoverUri(record.title, record.author)
            if result != None:
                record.cover = result
                print("✓ Book Cover", coverCounter, "/", coverCount, " has been sent, for", record.title)
            else:
                record.cover = no_cover_img
                print("× Book Cover", coverCounter, "/", coverCount, " coulnd't be found. Please replace the placeholder imge with original bookcover manually for", record.title)
        else:
            print("~ Book Cover", coverCounter, "/", coverCount, " is already existing, for", record.title)
        coverCounter += 1


client = NotionClient(token_v2= NOTION_TOKEN)
cv = client.get_collection_view(NOTION_TABLE_ID)
allRows = cv.collection.get_rows()
print(cv.parent.views)
ch = KindleClippings(CLIPPINGS_FILE)

# This should be called after upload. And this cover generator can be called separately.
generateBookCovers(cv)