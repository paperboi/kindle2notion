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
        clipCollection = []
        for i, eachClipping in enumerate(allClippings):
            if '- Your Highlight at location ' in eachClipping:
                eachClipping = eachClipping.strip().split("\n")
                # print(eachClipping[0])
                # import pdb; pdb.set_trace()
                title_author = eachClipping[0].replace('(', '|').replace(')', '')
                # print(title_author)
                # import pdb; pdb.set_trace()
                title, author = title_author.split('|')
                title = title.strip()
                location, addedOn = eachClipping[1].strip().split('|')
                location = location.replace('- Your Highlight at location ', '').replace(' ', '')
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                lastClip = {
                    'Title': title,
                    'Author': author,
                    'Page': None,
                    'Location': location,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                    }
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)

            elif '- Your Note on location ' in eachClipping:
                eachClipping = eachClipping.strip().split("\n")
                # print(eachClipping[0])
                # import pdb; pdb.set_trace()
                title_author = eachClipping[0].replace('(', '|').replace(')', '')
                # print(title_author)
                # import pdb; pdb.set_trace()
                title, author = title_author.split('|')
                title = title.strip()
                location, addedOn = eachClipping[1].strip().split('|')
                location = location.replace('- Your Note on location ', '').replace(' ', '')
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                lastClip = {
                    'Title': title,
                    'Author': author,
                    'Page': None,
                    'Location': location,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                    }
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)

            elif '- Your Highlight on page ' in eachClipping and 'location ' in eachClipping:
                eachClipping = eachClipping.strip().split("\n")
                # print(eachClipping[0])
                # import pdb; pdb.set_trace()
                title_author = eachClipping[0].replace('(', '|').replace(')', '')
                # print(title_author)
                title, author = title_author.split('|')
                title = title.strip()
                # import pdb; pdb.set_trace()
                page, location, addedOn = eachClipping[1].strip().split('|')
                page = page.replace('- Your Highlight on page ', '').replace(' ', '')
                location = location.replace(' location ', '').replace(' ','')
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                lastClip = {
                    'Title': title,
                    'Author': author,
                    'Page': None,
                    'Location': location,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                    }
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)

            elif '- Your Note on page ' in eachClipping and 'location ' in eachClipping:
                eachClipping = eachClipping.strip().split("\n")
                # print(eachClipping[0])
                # import pdb; pdb.set_trace()
                title_author = eachClipping[0].replace('(', '|').replace(')', '')
                title, author = title_author.split('|')
                title = title.strip()
                # print(title_author)
                # import pdb; pdb.set_trace()
                page, location, addedOn = eachClipping[1].strip().split('|')
                page = page.replace('- Your Note on page ', '').replace(' ', '')
                location = location.replace(' location ', '').replace(' ','')
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                lastClip = {
                    'Title': title,
                    'Author': author,
                    'Page': None,
                    'Location': location,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                    }
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)

            elif '- Your Highlight on page ' in eachClipping and 'location ' not in eachClipping:
                eachClipping = eachClipping.strip().split("\n")
                # print(eachClipping[0])
                # import pdb; pdb.set_trace()
                title = eachClipping[0]
                title = title.strip()
                # print(title_author)
                # title, author = title_author.split('|')
                # import pdb; pdb.set_trace()
                page, addedOn = eachClipping[1].strip().split('|')
                page = page.replace('- Your Highlight on page ', '').replace(' ', '')
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                lastClip = {
                    'Title': title,
                    'Author': author,
                    'Page': None,
                    'Location': location,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                    }
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)

            elif '- Your Note on page ' in eachClipping and 'location ' not in eachClipping:
                eachClipping = eachClipping.strip().split("\n")
                # print(eachClipping[0])
                # import pdb; pdb.set_trace()
                title = eachClipping[0]
                title = title.strip()
                # title, author = title_author.split('|')
                # print(title_author)
                # import pdb; pdb.set_trace()
                page, addedOn = eachClipping[1].strip().split('|')
                page = page.replace('- Your Note on page ', '').replace(' ', '')
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                lastClip = {
                    'Title': title,
                    'Author': author,
                    'Page': None,
                    'Location': location,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                    }
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)

            else:
                # Bookmark - ignore
                continue
        return clipCollection

    def _getClipping(self):
        for i in self.clippings:
            yield i
    
    def _lenClippings(self):
        return len(self.clippings)

    # def _titleAlreadyExists(title):
    #     global allRows
    #     if allRows == []:
    #         return False
    #     for eachRow in allRows:
    #         if title == eachRow.title:
    #             return (True, eachRow.id)
    #     print(f"Adding {itemURL} to the list")
    #     return False

    def addToNotion(self, lastClip):
        added = False
        global cv
        allRows = cv.collection.get_rows()
        # import pdb; pdb.set_trace()
        if allRows != []:
            for eachRow in allRows:
                # import pdb; pdb.set_trace()
                if lastClip['Title'] == eachRow.title:
                    parentPage = client.get_block(eachRow.id)
                    if lastClip['Location'] != None:
                        parentPage.children.add_new(
                            TextBlock,
                            title = "Location: " + lastClip['Location'] + "\tDate Added: " +  str(lastClip['Date Added'])
                        )
                    else:
                        parentPage.children.add_new(
                            TextBlock,
                            title = "Page: " + lastClip['Page'] + "\tDate Added: " +  str(lastClip['Date Added'])
                        )

                    parentPage.children.add_new(
                        QuoteBlock,
                        title = lastClip['Clipping']
                        )
                    # import pdb; pdb.set_trace()
                    eachRow.highlights +=1
                    eachRow.last_highlighted = NotionDate(lastClip['Date Added']) # dddd, dd MMMM yyyy HH:mm:ss
                    eachRow.last_synced = NotionDate(datetime.now())
                    added = True
        if added == False:
            row = cv.collection.add_row()
            row.title = lastClip['Title']
            row.author = lastClip['Author']
            row.highlights = 1
            # import pdb; pdb.set_trace()
            parentPage = client.get_block(row.id)
            if lastClip['Location'] != None:
                parentPage.children.add_new(
                    TextBlock,
                    title = "Location: " + lastClip['Location'] + "\tDate Added: " +  str(lastClip['Date Added'])
                )
            else:
                parentPage.children.add_new(
                    TextBlock,
                    title = "Page: " + lastClip['Page'] + "\tDate Added: " +  str(lastClip['Date Added'])
                )
            parentPage.children.add_new(
                QuoteBlock,
                title = lastClip['Clipping']
            )
            row.last_highlighted = NotionDate(lastClip['Date Added']) # dddd, dd MMMM yyyy HH:mm:ss
            row.last_synced = NotionDate(datetime.now())

client = NotionClient(token_v2= NOTION_TOKEN)
cv = client.get_collection_view(NOTION_TABLE_ID)
allRows = cv.collection.get_rows()
print(cv.parent.views)

ch = KindleClippings(CLIPPINGS_FILE)
ch._getClipping()
# addToNotion(allClippings)