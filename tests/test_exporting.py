from kindle2notion.exporting import _prepare_aggregated_text_for_one_book


def test_prepare_aggregated_text_for_one_book():
    # Given
    highlights = [('This is an example highlight.', '1', '100', 'Thursday, 29 April 2021 12:31:29 AM'),
                  ('This is a second example highlight.', '2', '200', 'Friday, 30 April 2021 12:31:29 AM')]

    expected = ('This is an example highlight.\n(*Page: 1*  *Location: 100*)\n\n'
                'This is a second example highlight.\n(*Page: 2*  *Location: 200*)\n\n',
                'Friday, 30 April 2021 12:31:29 AM')

    # When
    actual = _prepare_aggregated_text_for_one_book(highlights)

    # Then
    assert expected == actual
