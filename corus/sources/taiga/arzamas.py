# coding: utf-8

from __future__ import unicode_literals

import re
from datetime import datetime

from .common import (
    Author,
    Meta,
    load_tar_metas,
    load_tar_texts,
    merge_metas,
)


# {'About_author': '',
#  'Author_profession': 'Кандидат исторических наук. Креативный директор Фонда Егора Гайдара. Один из\xa0участников сетевого проекта «Прожито», создающего полный электронный корпус дневников советского времени.',
#  'URL': 'http://arzamas.academy/mag/427-chapter7Историк советской литературы и\xa0культуры',
#  'author': 'Илья Венявкин',
#  'id': '427',
#  'source': 'Arzamas',
#  'tags': "['Документ', 'СССР']",
#  'textdate': '27.04.2017',
#  'theme': "['Литература', 'История']",
#  'title': 'Советский писатель внутри Большого террора. Глава 7  •  '}


def parse_metas(items):
    for item in items:
        id = item['id']
        timestamp = datetime.strptime(item['textdate'], '%d.%m.%Y')
        tags = eval(item['tags'])
        themes = eval(item['theme'])
        name = item['author'] or None
        profession = item['Author_profession'] or None
        about = item['About_author'] or None
        author = Author(
            name=name,
            profession=profession,
            about=about
        )
        title = item['title'].strip(u'• ')
        url = item['URL']
        yield Meta(
            id=id,
            timestamp=timestamp,
            tags=tags,
            themes=themes,
            author=author,
            title=title,
            url=url
        )


def load_taiga_arzamas_metas(path, offset=0, count=1):
    items = load_tar_metas(path, '*/metatable.csv', offset, count=1)
    return parse_metas(items)


# home/tsha/Arzamas/texts/arzamas_449.txt
# home/tsha/Arzamas/texts/arzamas_450.txt
# home/tsha/Arzamas/texts/arzamas_452.txt


def parse_id(name):
    match = re.search(r'arzamas_(\d+)\.txt', name)
    return match.group(1)


def load_taiga_arzamas(path, metas=None, offset=144896, count=311):
    records = load_tar_texts(path, '*/texts/*.txt', offset, count, parse_id)
    return merge_metas(records, metas)


__all__ = [
    'load_taiga_arzamas_metas',
    'load_taiga_arzamas'
]
