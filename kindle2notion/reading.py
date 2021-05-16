import unicodedata


def read_raw_clippings(clippings_file):
    raw_clippings = open(clippings_file, 'r', encoding='utf-8-sig').read()
    raw_clippings = unicodedata.normalize('NFKD', raw_clippings)
    return raw_clippings
