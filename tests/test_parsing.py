from kindle2notion.parsing import get_page_or_and_loc, deal_with_exceptions_in_author_name, \
    deal_with_exceptions_in_title, parse_clippings


def test_parse_clippings():
    # Given
    with open('test_data/expected_clippings.txt', 'r') as f:
        all_clippings = f.read()

    expected = {'What You Do Is Who You Are: How to Create Your Business Culture': {'author': 'Ben Horowitz',
                                                                                    'highlights': [(
                                                                                        'Because your culture is how your company makes decisions when you’re not there. It’s the set of assumptions your employees use to resolve the problems they face every day. It’s how they behave when no one is looking. If you don’t methodically set your culture, then two-thirds of it will end up being accidental, and the rest will be a mistake. So how do you design and shape these nearly invisible',
                                                                                        '11', '1', ''), (
                                                                                        'Because your culture is how your company makes decisions when you’re not there. It’s the set of assumptions your employees use to resolve the problems they face every day. It’s how they behave when no one is looking. If you don’t methodically set your culture, then two-thirds of it will end up being accidental, and the rest will be a mistake. So how do you design and shape these nearly invisible',
                                                                                        '11', '1', '')]},
                'Working Backwards': {'author': 'Colin Bryar', 'highlights': [(
                    'Taking part in every aspect of the business allowed him to communicate the Amazon philosophy informally to the relatively small group of employees.',
                    '3', '3', ''), (
                    'Like all good processes, it’s simple to understand, can be easily taught to new people, does not depend on scarce resources (such as a single individual), and has a feedback loop to ensure continual improvement.',
                    '34', '4', '')]},
                'Clean Architecture (Robert C. Martin Series)': {'author': 'Martin Robert C.', 'highlights': [(
                    'The first paradigm to be adopted (but not the first to be invented) was structured programming, which was discovered by Edsger Wybe Dijkstra in 1968.',
                    '22',
                    '2', ''),
                    (
                        'Structured programming imposes discipline on direct transfer of control.',
                        '22',
                        '2',
                        '')]}}

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
