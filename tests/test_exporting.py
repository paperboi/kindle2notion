from kindle2notion.exporting import prepare_aggregated_text_for_one_book


def test_prepare_notion_information_for_one_book():
    # Given
    highlights = [(
                 'Taking part in every aspect of the business allowed him to communicate the Amazon philosophy informally to the relatively small group of employees.',
                 '3', '3', ''), (
                 'Like all good processes, it’s simple to understand, can be easily taught to new people, does not depend on scarce resources (such as a single individual), and has a feedback loop to ensure continual improvement.',
                 '34', '4', '')]

    expected = ('Taking part in every aspect of the business allowed him to communicate the Amazon philosophy informally to the relatively small group of employees.\n(*Page: 3*	*Location: 3*)\n\n' \
               'Like all good processes, it’s simple to understand, can be easily taught to new people, does not depend on scarce resources (such as a single individual), and has a feedback loop to ensure continual improvement.\n(*Page: 34*	*Location: 4*)\n\n', '')

    # When
    actual = prepare_aggregated_text_for_one_book(highlights)

    # Then
    assert expected == actual
