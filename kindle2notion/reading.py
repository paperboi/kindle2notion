from pathlib import Path


def read_raw_clippings(clippings_file_path: Path) -> str:
    try:
        raw_clippings_text = open(clippings_file_path, "r", encoding="utf-8-sig").read()
        raw_clippings_text = raw_clippings_text.encode("ascii").decode()
    except UnicodeEncodeError:
        print('UnicodeEncodeError, encoding data with utf-8')
        raw_clippings_text = open(clippings_file_path, "r", encoding="utf-8").read()
        raw_clippings_text = raw_clippings_text.encode("UTF8").decode()
    return raw_clippings_text
