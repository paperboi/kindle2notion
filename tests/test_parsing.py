from kindle2notion.parsing import parse_raw_clippings_text, _parse_author_and_title, _parse_page_location_and_date, \
    _add_parsed_items_to_books_dict
from kindle2notion.reading import read_raw_clippings
from kindle2notion.settings import TEST_CLIPPINGS_FILE


def test_parse_raw_clippings_text_should_return_a_dict_with_all_the_parsed_information():
    # Given
    raw_clippings_text = read_raw_clippings(TEST_CLIPPINGS_FILE)

    expected = {'Title 1: A Great Book': {'author': 'Ben Horowitz',
                                          'highlights': [('This is test highlight 1.', '11', '111-114', ''),
                                                         ('This is test highlight 2.', '11', '111-114', '')]},
                'Title 2 Is Good Too': {'author': 'Colin Bryar',
                                        'highlights': [('This is test highlight 3.', '3', '184-185', ''),
                                                       ('This is test highlight 4.', '34', '682-684', '')]},
                'Title 3 Is Clean (Robert C. Martin Series)': {'author': 'Martin Robert C.',
                                                               'highlights': [
                                                                   ('This is test highlight 5.', '22', '559-560', ''),
                                                                   ('This is test highlight 6.', '22', '564-565', '')]}}

    # When
    actual = parse_raw_clippings_text(raw_clippings_text)

    # Then
    assert expected == actual


def test_parse_author_and_title_case_1():
    # Given
    raw_clipping_list = ['Relativity (Einstein, Albert)',
                         '- Your Highlight on page 3 | Location 184-185 | Added on Friday, April 30, 2021 12:31:29 AM',
                         '',
                         'This is a test highlight.']
    expected = ('Albert Einstein', 'Relativity')

    # When
    actual = _parse_author_and_title(raw_clipping_list)

    # Then
    assert expected == actual


def test_parse_author_and_title_case_2():
    # Given
    raw_clipping_list = ['Relativity (Albert Einstein)',
                         '- Your Highlight on page 3 | Location 184-185 | Added on Friday, April 30, 2021 12:31:29 AM',
                         '',
                         'This is a test highlight.']
    expected = ('Albert Einstein', 'Relativity')

    # When
    actual = _parse_author_and_title(raw_clipping_list)

    # Then
    assert expected == actual


def test_parse_author_and_title_case_3():
    # Given
    raw_clipping_list = ['Candide (Voltaire (François-Marie Arouet))',
                         '- Your Highlight on page 3 | Location 184-185 | Added on Friday, April 30, 2021 12:31:29 AM',
                         '',
                         'This is a test highlight.']
    expected = ('Voltaire (François-Marie Arouet)', 'Candide')

    # When
    actual = _parse_author_and_title(raw_clipping_list)

    # Then
    assert expected == actual


def test_parse_author_and_title_case_4():
    # Given
    raw_clipping_list = ['Age of Louis XIV, The (Voltaire (François-Marie Arouet))',
                         '- Your Highlight on page 3 | Location 184-185 | Added on Friday, April 30, 2021 12:31:29 AM',
                         '',
                         'This is a test highlight.']
    expected = ('Voltaire (François-Marie Arouet)', 'The Age of Louis XIV')

    # When
    actual = _parse_author_and_title(raw_clipping_list)

    # Then
    assert expected == actual


def test_parse_author_and_title_case_5():
    # Given
    raw_clipping_list = ['The Mysterious Disappearance of Leon (I Mean Noel) (Ellen Raskin)',
                         '- Your Highlight on page 3 | Location 184-185 | Added on Friday, April 30, 2021 12:31:29 AM',
                         '',
                         'This is a test highlight.']
    expected = ('Ellen Raskin', 'The Mysterious Disappearance of Leon (I Mean Noel)')

    # When
    actual = _parse_author_and_title(raw_clipping_list)

    # Then
    assert expected == actual


def test_parse_page_location_and_date_case_1():
    # Given
    raw_clipping_list = ['Relativity (Albert Einstein)',
                         '- Your Highlight on page 3 | Location 184-185 | Added on Friday, April 30, 2021 12:31:29 AM',
                         '',
                         'This is a test highlight.']
    expected = ('3', '184-185', '')

    # When
    actual = _parse_page_location_and_date(raw_clipping_list)

    # Then
    assert expected == actual


def test_parse_page_location_and_date_case_2():
    # Given
    raw_clipping_list = ['Relativity (Albert Einstein)',
                         '- Your Highlight on page 3 | Location 184-185',
                         '',
                         'This is a test highlight.']
    expected = ('3', '184-185', '')

    # When
    actual = _parse_page_location_and_date(raw_clipping_list)

    # Then
    assert expected == actual


def test_parse_page_location_and_date_case_3():
    # Given
    raw_clipping_list = ['Relativity (Albert Einstein)',
                         'Location 184-185 | Added on Friday, April 30, 2021 12:31:29 AM',
                         '',
                         'This is a test highlight.']
    expected = ('', '184-185', '')

    # When
    actual = _parse_page_location_and_date(raw_clipping_list)

    # Then
    assert expected == actual


def test_parse_page_location_and_date_case_4():
    # Given
    raw_clipping_list = ['Relativity (Albert Einstein)',
                         '- Your Highlight on page 3 | Added on Friday, April 30, 2021 12:31:29 AM',
                         '',
                         'This is a test highlight.']
    expected = ('3', '', '')

    # When
    actual = _parse_page_location_and_date(raw_clipping_list)

    # Then
    assert expected == actual


# TODO: rename all tests with appropriate when


def test_add_parsed_items_to_books_dict_when_book_does_not_exist():
    # Given
    books = {}
    title = 'Relativity'
    author = 'Albert Einstein'
    highlight = 'This is a first highlight.'
    page = '1'
    location = '100'
    date = 'monday'

    expected = {'Relativity': {'author': 'Albert Einstein',
                               'highlights': [('This is a first highlight.', '1', '100', 'monday')]}}

    # When
    actual = _add_parsed_items_to_books_dict(books, title, author, highlight, page, location, date)

    # Then
    assert expected == actual


def test_add_parsed_items_to_books_dict_when_book_exists():
    # Given
    books = {'Relativity': {'author': 'Albert Einstein',
                            'highlights': [('This is a first highlight.', '1', '100', 'monday')]}}
    title = 'Relativity'
    author = 'Albert Einstein'
    highlight = 'This is a second highlight.'
    page = '2'
    location = '200'
    date = 'tuesday'

    expected = {'Relativity': {'author': 'Albert Einstein',
                               'highlights': [('This is a first highlight.', '1', '100', 'monday'),
                                              ('This is a second highlight.', '2', '200', 'tuesday')]}}

    # When
    actual = _add_parsed_items_to_books_dict(books, title, author, highlight, page, location, date)

    # Then
    assert expected == actual
