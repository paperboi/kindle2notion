from kindle2notion import get_all_clippings, parse_clippings, prepare_notion_information_for_one_book
from settings import TEST_CLIPPINGS_FILE


def test_get_all_clippings():
    # Given
    with open('expected_clippings.txt', 'r') as f:
        expected = f.read()

    # When
    actual = get_all_clippings(TEST_CLIPPINGS_FILE)

    # Then
    assert expected == actual


def test_parse_clippings():
    # Given
    with open('expected_clippings.txt', 'r') as f:
        all_clippings = f.read()

    expected = ({'What You Do Is Who You Are: How to Create Your Business Culture': {'author': 'Ben Horowitz',
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
                         '')]}},
                1)

    # When
    actual = parse_clippings(all_clippings)

    print(actual)

    # Then
    assert expected == actual


def test_prepare_notion_information_for_one_book():
    # Given
    books = {'What You Do Is Who You Are: How to Create Your Business Culture': {'author': 'Ben Horowitz',
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
    title = 'What You Do Is Who You Are: How to Create Your Business Culture'

    expected = (
    'Because your culture is how your company makes decisions when you’re not there. It’s the set of assumptions your employees use to resolve the problems they face every day. It’s how they behave when no one is looking. If you don’t methodically set your culture, then two-thirds of it will end up being accidental, and the rest will be a mistake. So how do you design and shape these nearly invisible\n(*Page: 11*\t*Location: 1*)\n\nBecause your culture is how your company makes decisions when you’re not there. It’s the set of assumptions your employees use to resolve the problems they face every day. It’s how they behave when no one is looking. If you don’t methodically set your culture, then two-thirds of it will end up being accidental, and the rest will be a mistake. So how do you design and shape these nearly invisible\n(*Page: 11*\t*Location: 1*)\n\n',
    'Ben Horowitz', '', 2)

    # When
    actual = prepare_notion_information_for_one_book(books, title)

    # Then
    assert expected == actual
