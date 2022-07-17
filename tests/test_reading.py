from pathlib import Path
from kindle2notion.reading import read_raw_clippings


def test_read_raw_clippings_should_return_all_clippings_data_as_string():
    # Given
    test_clippings_file_path = (
        Path(__file__).parent.absolute() / "test_data/Test Clippings.txt"
    )

    expected = """Title 1: A Great Book (Horowitz, Ben)
- Your Highlight on page 11 | Location 111-114 | Added on Tuesday, September 22, 2020 9:23:48 AM

This is test highlight 1.
==========
Title 1: A Great Book (Horowitz, Ben)
- Your Highlight on page 11 | Location 111-114 | Added on Tuesday, September 22, 2020 9:24:04 AM

This is test highlight 2.
==========
Title 2 Is Good Too (Bryar, Colin)
- Your Highlight on page 3 | Location 184-185 | Added on Friday, April 30, 2021 12:31:29 AM

This is test highlight 3.
==========
Title 2 Is Good Too (Bryar, Colin)
- Your Highlight on page 34 | Location 682-684 | Added on Friday, April 30, 2021 3:14:33 PM

This is test highlight 4.
==========
Title 3 Is Clean (Robert C. Martin Series) (C., Martin Robert)
- Your Highlight on page 22 | Location 559-560 | Added on Saturday, May 15, 2021 10:25:42 PM

This is test highlight 5.
==========
Title 3 Is Clean (Robert C. Martin Series) (C., Martin Robert)
- Your Highlight on page 22 | Location 564-565 | Added on Saturday, May 15, 2021 10:26:26 PM

This is test highlight 6.
=========="""

    # When
    actual = raw_clippings_text = read_raw_clippings(test_clippings_file_path)

    # Then
    assert expected == actual
