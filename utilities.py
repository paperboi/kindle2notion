from requests import get

# Get Cover Image
NO_COVER_IMG = "https://via.placeholder.com/150x200?text=No%20Cover"

def getBookCoverURI(title, author):
    reqURI = "https://www.googleapis.com/books/v1/volumes?q="
    
    if title == None: return
    
    reqURI += "intitle:" + title
    
    if author != None:
        reqURI += "+inauthor:" + author

    response = get(reqURI).json().get("items", [])
    if len(response) > 0:
        return response[0].get("volumeInfo", {}).get("imageLinks", {}).get("thumbnail")
    
    return

# Initializing Special chars for text formatting
ITALIC = "*"