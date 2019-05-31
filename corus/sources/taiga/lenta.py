# coding: utf-8

from __future__ import unicode_literals

from datetime import datetime

from .common import (
    Meta,
    load_tar_metas,
    load_tar_texts,
    patch_month,
    merge_metas
)


# {'author': '',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '8 марта 2011',
#   'magazine': '',
#   'segment': 'Lenta',
#   'source': 'https://lenta.ru/news/2011/03/08/hobgoblin/',
#   'tags': '',
#   'textdiff': '',
#   'textid': '20110308hobgoblin',
#   'textname': 'HBO запустит сериал о волшебной войне с Гитлером',
#   'textregion': '',
#   'textrubric': 'Культура',
#   'time': '14:33'},


LENTA_MONTHS = {
    'января': 'Jan',
    'февраля': 'Feb',
    'марта': 'Mar',
    'апреля': 'Apr',
    'мая': 'May',
    'июня': 'Jun',
    'июля': 'Jul',
    'августа': 'Aug',
    'сентября': 'Sep',
    'октября': 'Oct',
    'ноября': 'Nov',
    'декабря': 'Dec',
}


def parse_metas(items):
    for item in items:
        id = item['textid']

        date, time, timestamp = item['date'], item['time'], None
        if date and time:
            timestamp = patch_month(date, LENTA_MONTHS) + time
            timestamp = datetime.strptime(timestamp, '%d %b %Y%H:%M')

        title = item['textname']
        rubric = item['textrubric']
        url = item['source'] or None
        yield Meta(
            id=id,
            timestamp=timestamp,
            title=title,
            rubric=rubric,
            url=url
        )


def load_taiga_lenta_metas(path, offset=0, count=1):
    items = load_tar_metas(path, '*/newmetadata.csv', offset, count)
    return parse_metas(items)


# home/tsha/Lenta/texts/20100101three.txt
# home/tsha/Lenta/texts/20100101tomsk.txt
# home/tsha/Lenta/texts/20100101urus.txt


def load_taiga_lenta(path, metas=None, offset=12800000, count=36446):
    records = load_tar_texts(path, '*/texts/*.txt', offset, count)
    return merge_metas(records, metas)


__all__ = [
    'load_taiga_lenta_metas',
    'load_taiga_lenta'
]
