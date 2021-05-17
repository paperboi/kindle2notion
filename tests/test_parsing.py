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


def test_parse_author_and_title_case_should_parse_the_author_and_title_when_the_author_name_is_formatted_with_a_comma():
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


def test_parse_author_and_title_case_should_parse_the_author_and_title_when_the_author_name_is_first_name_last_name():
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


def test_parse_author_and_title_case_should_parse_the_author_and_title_when_there_are_parentheses_in_the_author_name():
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


def test_parse_author_and_title_case_should_parse_the_author_and_title_when_there_is_a_The_at_the_end_of_the_title():
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


def test_parse_author_and_title_case_should_parse_the_author_and_title_when_there_are_parentheses_in_the_title():
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


def test_parse_page_location_and_date_should_parse_the_page_location_and_date_when_there_are_all_three():
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


def test_parse_page_location_and_date_should_parse_the_page_and_location_when_there_is_no_date():
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


def test_parse_page_location_and_date_should_parse_the_location_and_date_when_there_is_no_page():
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


def test_parse_page_location_and_date_should_parse_the_page_and_date_when_there_is_no_location():
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


# TODO: In tests above, refacto the functions to include the dates


def test_add_parsed_items_to_books_dict_should_add_the_parsed_items_when_the_book_is_not_already_in_the_books_dict():
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


def test_add_parsed_items_to_books_dict_should_add_the_parsed_items_when_the_book_is_already_in_the_books_dict():
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
