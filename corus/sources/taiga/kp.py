# coding: utf8

from datetime import datetime

from .common import (
    Author,
    Meta,
    load_tar_metas,
    load_tar_texts,
    merge_metas
)


# {'author': 'Мария ГОШИНА',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '2017-01-20',
#   'magazine': '',
#   'segment': 'KP',
#   'source': 'http://www.kp.ru/online/news/2632060/',
#   'tags': '',
#   'textdiff': '',
#   'textid': '10@2632060',
#   'textname': 'В Саратове спасатели помогли родственникам попасть в квартиру пенсионерки',
#   'textregion': 'www.saratov.kp.ru',
#   'textrubric': 'Общество>Общество',
#   'time': '09:27:00+03:00'},


def parse_metas(items):
    for item in items:
        id = item['textid']
        timestamp = item['date'] + item['time'][:8]
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d%H:%M:%S')

        name = item['author'] or None
        author = Author(name=name)

        rubric = item['textrubric']
        title = item['textname']
        url = item['source']
        yield Meta(
            id=id,
            timestamp=timestamp,
            rubric=rubric,
            author=author,
            title=title,
            url=url
        )


def load_taiga_kp_metas(path, offset=0, count=1):
    items = load_tar_metas(path, '*/newmetadata.csv', offset, count)
    return parse_metas(items)


# home/tsha/KP/texts/10@2598286.txt
# home/tsha/KP/texts/10@2598287.txt
# home/tsha/KP/texts/10@2598289.txt


def load_taiga_kp(path, metas=None, offset=13042176, count=45503):
    records = load_tar_texts(path, '*/texts/*.txt', offset, count)
    return merge_metas(records, metas)


__all__ = [
    'load_taiga_kp_metas',
    'load_taiga_kp'
]
