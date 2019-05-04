# coding: utf8

from .common import (
    Meta,
    load_tar_metas,
    load_tar_texts,
    parse_filename_id,
    merge_metas
)


# [{'filepath': 'Heroes - 3x12 - Our Father.HDTV.LOL.en.txt',
#   'id': '8940',
#   'languages': 'en',
#   'title': 'Heroes - 3x12 - Our Father.HDTV.LOL.en.srt'},
#  {'filepath': 'Friends - 3x17 - The One Without The Ski Trip.ru.txt',
#   'id': '7553',
#   'languages': 'ru',
#   'title': 'Friends - 3x17 - The One Without The Ski Trip.ru.srt'},


def parse_metas(items):
    for item in items:
        id = parse_filename_id(item['filepath'])
        lang = item['languages']
        title = item['title']
        yield Meta(
            id=id,
            lang=lang,
            title=title
        )


def load_taiga_subtitles_metas(path, offset=0, count=1):
    items = load_tar_metas(path, '*/metatable.csv', offset, count)
    return parse_metas(items)


# home/tsha/Subtitles/texts/12 Monkeys/12 Monkeys - 1x01 - Splinter.HDTV.KILLERS.en.txt
# home/tsha/Subtitles/texts/12 Monkeys/12 Monkeys - 1x01 - Splinter.HDTV.KILLERS.ru.txt


def load_taiga_subtitles(path, metas=None, offset=2113024, count=19011):
    records = load_tar_texts(path, '*/texts/*.txt', offset, count)
    return merge_metas(records, metas)
