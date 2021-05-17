import unicodedata


def read_raw_clippings(clippings_file_path: str) -> str:
    raw_clippings_text = open(clippings_file_path, 'r', encoding='utf-8-sig').read()
    raw_clippings_text = unicodedata.normalize('NFKD', raw_clippings_text)
    return raw_clippings_text
