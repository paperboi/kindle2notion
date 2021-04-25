from requests import get

no_cover_img = "https://via.placeholder.com/150x200?text=No%20Cover"

def getBookCoverUri(title, author):
    req_uri = "https://www.googleapis.com/books/v1/volumes?q="
    
    if title == None: return
    
    req_uri += "intitle:" + title
    
    if author != None:
        req_uri += "+inauthor:" + author

    response = get(req_uri).json().get("items", [])
    if len(response) > 0:
        return response[0].get("volumeInfo", {}).get("imageLinks", {}).get("thumbnail")
    
    return