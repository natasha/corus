# coding: utf8

from __future__ import unicode_literals

from datetime import datetime

from .common import (
    Author,
    Meta,
    load_tar_metas,
    load_tar_texts,
    patch_month,
    merge_metas,
)


# {'author': 'Владимир Королев',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '21 Янв. 2017',
#   'magazine': '',
#   'segment': 'nplus1',
#   'source': 'https://nplus1.ru/news/2017/01/21/Asphaltene-3d',
#   'tags': '',
#   'textdiff': '5.2',
#   'textid': '20170121Asphaltene-3d',
#   'textname': '«Архипелаги» асфальтенов ощупали в 3D',
#   'textregion': '',
#   'textrubric': 'Наука',
#   'time': '17:34'},


NPLUS1_MONTHS = {
    'Янв.': 'Jan',
    'Фев.': 'Feb',
    'Март': 'Mar',
    'Апр.': 'Apr',
    'Май': 'May',
    'Июнь': 'Jun',
    'Июль': 'Jul',
    'Авг.': 'Aug',
    'Сен.': 'Sep',
    'Окт.': 'Oct',
    'Нояб.': 'Nov',
    'Дек.': 'Dec',
}


def parse_metas(items):
    for item in items:
        id = item['textid']

        timestamp, date, time = None, item['date'], item['time']
        if date and time:
            timestamp = patch_month(date, NPLUS1_MONTHS) + time
            timestamp = datetime.strptime(timestamp, '%d %b %Y%H:%M')

        name = item['author'] or None
        author = Author(name=name)

        title = item['textname']
        rubric = item['textrubric'] or None
        url = item['source']
        yield Meta(
            id=id,
            timestamp=timestamp,
            author=author,
            title=title,
            rubric=rubric,
            url=url
        )


def load_taiga_nplus1_metas(path, offset=0, count=1):
    items = load_tar_metas(path, '*/newmetadata.csv', offset, count)
    return parse_metas(items)


# home/tsha/NPlus1/texts/20150320drone.txt
# home/tsha/NPlus1/texts/20150320nitrogen.txt
# home/tsha/NPlus1/texts/20150320silica.txt


def load_taiga_nplus1(path, metas=None, offset=1919488, count=7696):
    records = load_tar_texts(path, '*/texts/*.txt', offset, count)
    return merge_metas(records, metas)


__all__ = [
    'load_taiga_nplus1_metas',
    'load_taiga_nplus1'
]
