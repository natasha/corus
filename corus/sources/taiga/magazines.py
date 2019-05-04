# coding: utf8

import re
from datetime import datetime

from .common import (
    Meta,
    load_tar_metas,
    load_tar_texts,
    merge_metas,
)


# {'author': '',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '2007, 10',
#   'magazine': 'Знамя',
#   'segment': 'Журнальный зал',
#   'source': 'http://magazines.russ.ru/znamia/2007/10/tu26.html',
#   'tags': '',
#   'textdiff': '',
#   'textid': '50005',
#   'textname': 'Михаил Копелиович. Рецензия &amp;#8211; любовь моя',
#   'textregion': '',
#   'textrubric': 'article',
#   'time': ''},


def parse_metas(items):
    for item in items:
        id = item.get('textid')
        if not id:
            continue

        timestamp = item.get('date')
        if timestamp:
            try:
                timestamp = datetime.strptime(timestamp, '%Y, %m')
            except ValueError:
                # rare 2002, 7-8
                pass

        title = item['textname'] or None
        rubric = item.get('textrubric') or None

        url = None
        if 'source' in item:
            url = item['source']
            match = re.search(r'russ\.ru/([^/]+)', url)
            label = match.group(1)
            id = label + '_' + id

        yield Meta(
            id=id,
            timestamp=timestamp,
            title=title,
            rubric=rubric,
            url=url
        )


def load_taiga_magazines_metas(path, offset=0, count=36):
    items = load_tar_metas(path, '*/corpus_*_metadata.csv', offset, count)
    return parse_metas(items)


# home/tsha/Magazines/texts/corpus_arion_10658.txt
# home/tsha/Magazines/texts/corpus_arion_10659.txt


def parse_magazines_id(name):
    match = re.search(r'corpus_([\d\w_]+)\.txt', name)
    return match.group(1)


def load_taiga_magazines(path, metas=None, offset=7292416, count=39890):
    records = load_tar_texts(path, '*/texts/*.txt', offset, count)
    return merge_metas(records, metas)


__all__ = [
    'load_taiga_magazines_metas',
    'load_taiga_magazines'
]
