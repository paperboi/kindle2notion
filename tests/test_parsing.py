from kindle2notion.parsing import get_page_or_and_loc, deal_with_exceptions_in_author_name, \
    deal_with_exceptions_in_title, parse_clippings


def test_parse_clippings():
    # Given
    with open('test_data/expected_clippings.txt', 'r') as f:
        all_clippings = f.read()

    expected = {'Title 1: A Great Book': {'author': 'Ben Horowitz',
                                          'highlights': [('This is test highlight 1.', '11', '1', ''),
                                                         ('This is test highlight 2.', '11', '1', '')]},
                'Title 2 Is Good Too': {'author': 'Colin Bryar',
                                        'highlights': [('This is test highlight 3.', '3', '3', ''),
                                                       ('This is test highlight 4.', '34', '4', '')]},
                'Title 3 Is Clean (Robert C. Martin Series)': {'author': 'Martin Robert C.',
                                                               'highlights': [
                                                                   ('This is test highlight 5.', '22', '2', ''),
                                                                   ('This is test highlight 6.', '22', '2', '')]}}

    # When
    actual = parse_clippings(all_clippings)

    # Then
    assert expected == actual


def test_get_page_or_and_loc():
    # Given
    clipping = ['Working Backwards (Bryar, Colin)',
                '- Your Highlight on page 3 | Location 184-185 | Added on Friday, April 30, 2021 12:31:29 AM',
                '',
                'Taking part in every aspect of the business allowed him to communicate the Amazon philosophy informally to the relatively small group of employees.']

    expected = ('- Your Highlight on page 3', ['Location 184-185', 'Added on Friday, April 30, 2021 12:31:29 AM'])

    # When
    actual = get_page_or_and_loc(clipping)

    # Then
    assert expected == actual


def test_deal_with_exceptions_in_author_name_when_nominal():
    # Given
    author = 'BA SA'
    title = 'A Masterpiece'
    expected_author, expected_title = ('BA SA', 'A Masterpiece')

    # When
    actual_author, actual_title = deal_with_exceptions_in_author_name(author, title)

    # Then
    assert (expected_author, expected_title) == (actual_author, actual_title)


def test_deal_with_exceptions_in_author_name_when_comma_in_author_name():
    # Given
    author = 'Bryar, Colin'
    title = 'Working Backwards'
    expected_author, expected_title = ('Colin Bryar', 'Working Backwards')

    # When
    actual_author, actual_title = deal_with_exceptions_in_author_name(author, title)

    # Then
    assert (expected_author, expected_title) == (actual_author, actual_title)


def test_deal_with_exceptions_in_author_name_when_parentheses_in_author_name():
    # Given
    author = 'Voltaire (François-Marie Arouet'
    title = 'Random title)'
    expected_author, expected_title = ('Voltaire (François-Marie Arouet)', 'Random title')

    # When
    actual_author, actual_title = deal_with_exceptions_in_author_name(author, title)

    # Then
    assert (expected_author, expected_title) == (actual_author, actual_title)


def test_deal_with_exceptions_in_title_when_nominal():
    # Given
    title = 'Working Backwards'
    expected = 'Working Backwards'

    # When
    actual = deal_with_exceptions_in_title(title)

    # Then
    assert expected == actual


def test_deal_with_exceptions_in_title_when_exception():
    # Given
    title = 'Mysterious Disappearance of Leon (I Mean Noel), The'
    expected = 'The Mysterious Disappearance of Leon (I Mean Noel)'

    # When
    actual = deal_with_exceptions_in_title(title)

    # Then
    assert expected == actual
