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
        for eachClipping in allClippings:
            if '- Your Highlight at location ' in eachClipping:
                eachClipping = eachClipping.strip().split("\n")
                title_author = eachClipping[0].replace('(', '|').replace(')', '')
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
                title_author = eachClipping[0].replace('(', '|').replace(')', '')
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
                title_author = eachClipping[0].replace('(', '|').replace(')', '')
                title, author = title_author.split('|')
                title = title.strip()
                page, location, addedOn = eachClipping[1].strip().split('|')
                page = page.replace('- Your Highlight on page ', '').replace(' ', '')
                location = location.replace(' location ', '').replace(' ','')
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                lastClip = {
                    'Title': title,
                    'Author': author,
                    'Page': page,
                    'Location': location,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                    }
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)

            elif '- Your Note on page ' in eachClipping and 'location ' in eachClipping:
                eachClipping = eachClipping.strip().split("\n")
                title_author = eachClipping[0].replace('(', '|').replace(')', '')
                title, author = title_author.split('|')
                title = title.strip()
                page, location, addedOn = eachClipping[1].strip().split('|')
                page = page.replace('- Your Note on page ', '').replace(' ', '')
                location = location.replace(' location ', '').replace(' ','')
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                lastClip = {
                    'Title': title,
                    'Author': author,
                    'Page': page,
                    'Location': location,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                    }
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)

            elif '- Your Highlight on page ' in eachClipping and 'location ' not in eachClipping:
                eachClipping = eachClipping.strip().split("\n")
                title = eachClipping[0]
                title = title.strip()
                page, addedOn = eachClipping[1].strip().split('|')
                page = page.replace('- Your Highlight on page ', '').replace(' ', '')
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                lastClip = {
                    'Title': title,
                    'Author': author,
                    'Page': page,
                    'Location': None,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                    }
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)

            elif '- Your Note on page ' in eachClipping and 'location ' not in eachClipping:
                eachClipping = eachClipping.strip().split("\n")
                title = eachClipping[0]
                title = title.strip()
                page, addedOn = eachClipping[1].strip().split('|')
                page = page.replace('- Your Note on page ', '').replace(' ', '')
                dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]
                lastClip = {
                    'Title': title,
                    'Author': author,
                    'Page': page,
                    'Location': None,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                    }
                clipCollection.append(lastClip)
                self.addToNotion(lastClip)
                print(self._getClipping())

            else:
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