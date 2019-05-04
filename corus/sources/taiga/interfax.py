# coding: utf8

from datetime import datetime

from .common import (
    Meta,
    load_tar_metas,
    load_tar_texts,
    merge_metas
)


# {'author': '',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '2013-02-24',
#   'magazine': '',
#   'segment': 'Interfax',
#   'source': 'http://www.interfax.ru/russia/292151',
#   'tags': 'Кубань',
#   'textdiff': '',
#   'textid': 'russia292151',
#   'textname': '60 тысяч жителей Туапсинского района остались без электричества',
#   'textregion': '',
#   'textrubric': 'В России',
#   'time': '16:10'},


def parse_metas(items):
    for item in items:
        id = item['textid']

        timestamp = item['date'] + item['time']
        try:
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d%H:%M')
        except ValueError:
            # rare, date='' time='2011-09-12'
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d')

        title = item['textname']
        tags = item['tags']
        rubric = item.get('rubric')
        url = item['source']
        yield Meta(
            id=id,
            timestamp=timestamp,
            title=title,
            rubric=rubric,
            tags=tags,
            url=url
        )


def load_taiga_interfax_metas(path, offset=0, count=1):
    items = load_tar_metas(path, '*/newmetadata.csv', offset, count)
    return parse_metas(items)


# home/tsha/Interfax/texts/business225067.txt
# home/tsha/Interfax/texts/business225113.txt
# home/tsha/Interfax/texts/business225178.txt


def load_taiga_interfax(path, metas=None, offset=11447296, count=46429):
    records = load_tar_texts(path, '*/texts/*.txt', offset, count)
    return merge_metas(records, metas)


__all__ = [
    'load_taiga_interfax_metas',
    'load_taiga_interfax'
]
