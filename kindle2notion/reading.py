# import unicodedata
from pathlib import Path


def read_raw_clippings(clippings_file_path: Path) -> str:
    raw_clippings_text = open(clippings_file_path, "r", encoding="utf-8-sig").read()
    raw_clippings_text = raw_clippings_text.encode("ascii", errors="ignore").decode()
    return raw_clippings_text
