from kindle2notion.exporting import _prepare_aggregated_text_for_one_book


def test_prepare_notion_information_for_one_book():
    # Given
    highlights = [('This is an example highlight.', '3', '3', ''),
                  ('This is a second example highlight.', '34', '4', '')]

    expected = ('This is an example highlight.\n(*Page: 3*  *Location: 3*)\n\n'
                'This is a second example highlight.\n(*Page: 34*  *Location: 4*)\n\n', '')

    # When
    actual = _prepare_aggregated_text_for_one_book(highlights)

    # Then
    assert expected == actual
