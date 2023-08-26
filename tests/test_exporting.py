from kindle2notion.exporting import _prepare_aggregated_text_for_one_book


def test_prepare_aggregated_text_for_one_book_should_return_the_aggregated_text_when_highlight_date_is_disabled():
    # Given
    highlights = [
        (
            "This is an example highlight.",
            "1",
            "100",
            "Thursday, 29 April 2021 12:31:29 AM",
            False,
        ),
        (
            "This is a second example highlight.",
            "2",
            "200",
            "Friday, 30 April 2021 12:31:29 AM",
            True,
        ),
    ]

    expected = (
        [
            "This is an example highlight.\n* Page: 1, Location: 100\n\n",
            "> NOTE: \nThis is a second example highlight.\n* Page: 2, Location: 200\n\n",
        ],
        "Friday, 30 April 2021 12:31:29 AM",
    )

    # When
    actual = _prepare_aggregated_text_for_one_book(
        highlights, enable_highlight_date=False
    )
    print(actual)
    # Then
    assert expected == actual


def test_prepare_aggregated_text_for_one_book_should_return_the_aggregated_text_when_highlight_date_is_enabled():
    # Given
    highlights = [
        (
            "This is an example highlight.",
            "1",
            "100",
            "Thursday, 29 April 2021 12:31:29 AM",
            False,
        ),
        (
            "This is a second example highlight.",
            "2",
            "200",
            "Friday, 30 April 2021 12:31:29 AM",
            True,
        ),
    ]

    expected = (
        [
            "This is an example highlight.\n* Page: 1, Location: 100, Date Added: Thursday, 29 April 2021 12:31:29 AM\n\n",
            "> NOTE: \nThis is a second example highlight.\n* Page: 2, Location: 200, Date Added: Friday, 30 April 2021 12:31:29 AM\n\n",
        ],
        "Friday, 30 April 2021 12:31:29 AM",
    )

    # When
    actual = _prepare_aggregated_text_for_one_book(
        highlights, enable_highlight_date=True
    )
    print(actual)
    # Then
    assert expected == actual


def test_when_date_is_not_ampm_format_then_aggregated_text_should_return_appropiate_date():
    # Given
    highlights = [
        (
            "This is an example highlight.",
            "1",
            "100",
            "jueves, 24 de agosto de 2023 7:28:38",
            False,
        ),
        (
            "This is a second example highlight.",
            "2",
            "200",
            "viernes, 25 de agosto de 2023 7:28:38",
            True,
        ),
    ]

    expected = (
        [
            "This is an example highlight.\n* Page: 1, Location: 100, Date Added: jueves, 24 de agosto de 2023 7:28:38\n\n",
            "> NOTE: \nThis is a second example highlight.\n* Page: 2, Location: 200, Date Added: viernes, 25 de agosto de 2023 7:28:38\n\n",
        ],
        "viernes, 25 de agosto de 2023 7:28:38",
    )

    # When
    actual = _prepare_aggregated_text_for_one_book(
        highlights, enable_highlight_date=True
    )
    print(actual)
    # Then
    assert expected == actual


def test_when_date_is_not_ampm_format_then_aggregated_text_should_not_give_valueerror():
    pass