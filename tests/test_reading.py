from kindle2notion.reading import read_raw_clippings
from settings import TEST_CLIPPINGS_FILE


def test_read_raw_clippings():
    # Given
    with open('test_data/expected_clippings.txt', 'r') as f:
        expected = f.read()

    # When
    actual = read_raw_clippings(TEST_CLIPPINGS_FILE)

    # Then
    assert expected == actual
