import re

from dateparser import parse

from settings import ENABLE_HIGHLIGHT_DATE


def parse_clippings(raw_clippings):
    raw_clippings_list = raw_clippings.split('==========')
    print(f'Found {len(raw_clippings_list)} notes and highlights.\n')
    books = {}
    passed_clipping_count = 0

    for raw_clipping in raw_clippings_list:
        raw_clipping = raw_clipping.strip().split('\n')

        if is_valid_clipping(raw_clipping):
            author, title = parse_author_and_title(raw_clipping)
            page, location, date = parse_page_location_and_date(raw_clipping)
            highlight = raw_clipping[3]
            add_highlight_to_book_dict(author, books, title, page, location, date, highlight)
        else:
            passed_clipping_count += 1

    print(f'× Passed {passed_clipping_count} bookmarks or unsupported clippings.\n')
    return books


def is_valid_clipping(raw_clipping):
    return len(raw_clipping) >= 3


def parse_author_and_title(raw_clipping):
    author = (re.findall(r'\(.*?\)', raw_clipping[0]))[-1]
    author = author.removeprefix('(').removesuffix(')')
    title = raw_clipping[0].replace(author, '').strip().replace(u'\ufeff', '').replace(' ()', '')
    author, title = deal_with_exceptions_in_author_name(author, title)
    title = deal_with_exceptions_in_title(title)
    return author, title


def parse_page_location_and_date(raw_clipping):
    pageOrAndLoc, optLocAndDate = get_page_or_and_loc(raw_clipping)
    page = pageOrAndLoc[pageOrAndLoc.find('page'):].replace('page', '').strip()
    location = pageOrAndLoc[pageOrAndLoc.find('location'):].replace('location', '').strip()

    date = ''
    if ENABLE_HIGHLIGHT_DATE:
        addedOn = optLocAndDate[-1]
        date = parse(addedOn[addedOn.find('Added on'):].replace('Added on', '').strip())
    return page, location, date


def add_highlight_to_book_dict(author, books, title, page, location, date, highlight):
    if title not in books:
        books[title] = {'author': author, 'highlights': []}
    books[title]['highlights'].append((highlight, page, location, date))


def deal_with_exceptions_in_author_name(author, title):
    if '(' in author:
        author = author + ')'
        title = title.removesuffix(')')
    if ', ' in author:
        last_name, first_name = author.split(', ')
        author = first_name + ' ' + last_name
    return author, title


def deal_with_exceptions_in_title(title):
    if ', The' in title:
        title = 'The ' + title.replace(', The', '')
    return title


def get_page_or_and_loc(clipping):
    # Please regard this hack. This operation can return some pairs like (page and date), (location and date)
    # or 3 values: (page, location, date)
    second_line = clipping[1]
    pageOrAndLoc, *optLocAndDate = second_line.strip().split(' | ')
    return pageOrAndLoc, optLocAndDate
