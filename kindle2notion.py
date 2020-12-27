from notion.client import NotionClient
from notion.collection import NotionDate
from notion.block import QuoteBlock, TextBlock, PageBlock

from datetime import datetime
import string
import os
import unicodedata
from settings import CLIPPINGS_FILE, NOTION_TOKEN, NOTION_TABLE_ID

class KindleClippings(object):
    def __init__(self, clippingsFile):
        self.clippings = self._getAllClippings(clippingsFile)

    def _getAllClippings(self, clippingsFile):
        allClippings = open(clippingsFile, 'r', encoding="utf-8-sig").read()
        allClippings = unicodedata.normalize("NFKD", allClippings)
        return self._parseClippings(allClippings)

    def _parseClippings(self, allClippings):
        allClippings = allClippings.split("==========")
        total = len(allClippings)
        print("Found", total, "notes and highlights" )
        counter = 1
        clipCollection = []
        for eachClipping in allClippings:
            eachClipping = eachClipping.strip().split("\n")
            
            # Sometimes a null text or a bookmark can be selected as clipping. So check the array size;
            if len(eachClipping) >= 3:
                firstLine = eachClipping[0]
                secondLine = eachClipping[1] # Second line after = marks, for identifying type

                print("Processing note/highlight number", counter, "/", total, "from", firstLine)

                # TODO: Author name can be stated like "Voltaire (francois Marie Arouet)" So author name should be extracted with Regex.
                title_author = eachClipping[0].replace('(', '|').replace(')', '')
                
                # Converted author datatype from string to array for all type of notes. If author is single it'll be converted to string without comma
                title, *author = title_author.split('|')
                title = title.strip()

                # Please regard this hack. This operation can return some pairs like (page and date), (location and date)
                # or 3 values: (page, location, date)
                # We'll get last item for date.
                # Parameter Explanation
                # 1. pageOrAndLoc: page or and location: page or location & page and location can return
                # 2. optLocAndDate: Optionally Location can return and date can return or only date can return as array
                pageOrAndLoc, *optLocAndDate = secondLine.strip().split('|')

                addedOn = optLocAndDate[-1]
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]

                lastClip = {
                        'Title': title,
                        'Author': ",".join(author),
                        'Page': None,
                        'Location': None,
                        'Date Added': dateAdded,
                        'Clipping': clipping
                }
            
                # TODO: This conditions also can be reduced. New logic can check "Your X at/on location/page" and change it dynamically
                if '- Your Highlight at location ' in secondLine:
                    location = pageOrAndLoc.replace('- Your Highlight at location ', '').replace(' ', '')
                    lastClip["Location"] = location

                elif '- Your Note on location ' in secondLine:
                    location = pageOrAndLoc.replace('- Your Note on location ', '').replace(' ', '')
                    lastClip["Location"] = location

                elif '- Your Highlight on page ' in secondLine and 'location ' in secondLine:
                    page = pageOrAndLoc.replace('- Your Highlight on page ', '').replace(' ', '')
                    location = optLocAndDate[0].replace(' location ', '').replace(' ','')
                    lastClip["Page"] = page
                    lastClip["Location"] = location

                elif '- Your Note on page ' in secondLine and 'location ' in secondLine:
                    page = pageOrAndLoc.replace('- Your Note on page ', '').replace(' ', '')
                    location = optLocAndDate[0].replace(' location ', '').replace(' ','')
                    lastClip["Page"] = page
                    lastClip["Location"] = location

                elif '- Your Highlight on page ' in secondLine and 'location ' not in secondLine:
                    page = pageOrAndLoc.replace('- Your Highlight on page ', '').replace(' ', '')
                    lastClip["Page"] = page

                elif '- Your Note on page ' in secondLine and 'location ' not in secondLine:
                    page = pageOrAndLoc.replace('- Your Note on page ', '').replace(' ', '')
                    lastClip["Page"] = page
                    # TODO: Check this.
                    print(self._getClipping())
                
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)
                counter += 1

            else:
                # TODO: Bookmarks can be added to the service also ??
                print("Skipping bookmark number:", counter, "Because it's empty.")
                counter += 1
                continue

        return clipCollection

    def _getClipping(self):
        for i in self.clippings:
            yield i
    
    def _lenClippings(self):
        return len(self.clippings)
    
    def addNewClippingToRow(self, lastClip, row, titleExists):
        clipExists = False
        if not titleExists:
            row.title = lastClip['Title']
            row.author = lastClip['Author']
            row.highlights = 0        
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

    def addToNotion(self, lastClip):
        titleExists = False
        clipExists = False
        global cv
        allRows = cv.collection.get_rows()
        if allRows != []:
            for eachRow in allRows:
                if lastClip['Title'] == eachRow.title:
                    titleExists = True
                    row = eachRow
        if not titleExists:
            row = cv.collection.add_row()
            row.title = lastClip['Title']
            row.author = lastClip['Author']
            row.highlights = 0
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

client = NotionClient(token_v2= NOTION_TOKEN)
cv = client.get_collection_view(NOTION_TABLE_ID)
allRows = cv.collection.get_rows()
print(cv.parent.views)

ch = KindleClippings(CLIPPINGS_FILE)