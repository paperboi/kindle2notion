from notion.client import NotionClient
from notion.collection import NotionDate

from datetime import datetime
import os
import unicodedata
from settings import CLIPPINGS_FILE, NOTION_TOKEN, NOTION_PAGE_ID

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
        for eachClipping in enumerate(allClippings):
            eachClipping = eachClipping.strip().split("\n")
            title_author = eachClipping[0].replace('(', '|').replace(')', '').strip()
            title, author = title_author.split('|')
            clipping = eachClipping[3]

            if '- Your Highlight at location ' in eachClipping:
                page = None
                location, addedOn = eachClipping[1].strip().split('|')
                location = location.replace('- Your Highlight at location ', '').replace(' ', '')
            
            elif '- Your Highlight on page ' in eachClipping:
                page, location, addedOn = eachClipping[1].strip().split('|')
                page = page.replace('- Your Highlight on page ', '').replace(' ', '')
                location = location.replace(' location ', '').replace(' ','')

            elif '- Your Note on location ' in eachClipping:
                page = None
                location, addedOn = eachClipping[1].strip().split('|')
                location = location.replace('- Your Note on location ', '').replace(' ', '')

            elif '- Your Note on page ' in eachClipping:
                page, location, addedOn = eachClipping[1].strip().split('|')
                page = page.replace('- Your Note on page ', '').replace(' ', '')
                location = location.replace(' location ', '').replace(' ','')

            dateAdded = datetime.strptime(addedOn, ' Added on %A, %d %B %Y %X')

            clipCollection.append({
                'Title': title,
                'Author': author,
                'Page': page,
                'Location': location,
                'Date Added': dateAdded,
                'Clipping': clipping
                })
            self.addToNotion(clipCollection[:1])
        return clipCollection

    def _getClipping(self):
        for i in self.clippings:
            yield i
    
    def _lenClippings(self):
        return len(self.clippings)
    
    def addToNotion(self, parameter_list):
        pass

KindleClippings(CLIPPINGS_FILE)
# addToNotion(allClippings)