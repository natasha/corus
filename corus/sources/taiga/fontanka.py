# coding: utf8

import re
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
#   'date': '04.04.2015',
#   'magazine': '',
#   'segment': 'Fontanka',
#   'tags': 'Санкт-Петербург, Петербург, СПб, фонтанка, фонтанка.ру, АЖУР, Агентство Журналистских расследований, СМИ, новости, новости Петербурга, политика, экономика, криминал, Фонтанка, информация, события, город, культура,  политика,  бизнес,  общество,  происшествия,  спорт, свободное время, авто, недвижимость, зарубежная недвижимость, Охта центр, финансы, туризм, работа, особое мнениеhttp://www.fontanka.ru/2015/04/04/068/',
#   'textdiff': '',
#   'textid': '20150404068',
#   'textname': 'Минобороны: Россия не отстает от США в разработке лазерного оружия',
#   'textregion': '',
#   'textrubric': 'Технологии',
#   'time': '20:59'},


def parse_metas(items):
    for item in items:
        id = item['textid']
        # {'segment': 'Fontanka', 'textname': '&quot;', 'textid': '20100205145'}
        tags, url, rubric, title = (), None, None, None

        if 'date' in item and 'time' in item:
            timestamp = item['date'] + item['time']
            if timestamp:
                timestamp = datetime.strptime(timestamp, '%d.%m.%Y%H:%M')

        if 'tags' in item:
            tags = item['tags']
            match = re.search(r'(http://.+)$', tags)
            if match:
                url = match.group(1)
                tags = re.split(r',\s+', tags[:match.start()])

        rubric = item.get('textrubric')
        title = item.get('textname')
        yield Meta(
            id=id,
            timestamp=timestamp,
            tags=tags,
            rubric=rubric,
            title=title,
            url=url
        )


def load_taiga_fontanka_metas(path, offset=0, count=2017 - 2005 + 1):
    items = load_tar_metas(path, '*/metatable_*.csv', offset, count)
    return parse_metas(items)


# home/tsha/Fontanka/texts/2007/fontanka_20070101001.txt
# home/tsha/Fontanka/texts/2007/fontanka_20070101002.txt
# home/tsha/Fontanka/texts/2007/fontanka_20070101004.txt
# home/tsha/Fontanka/texts/2007/fontanka_20070101003.txt


def parse_id(name):
    match = re.search(r'fontanka_(\d+)\.txt', name)
    return match.group(1)


def load_taiga_fontanka(path, metas=None, offset=306359296, count=342683):
    records = load_tar_texts(path, '*/texts/*.txt', offset, count, parse_id)
    return merge_metas(records, metas)


__all__ = [
    'load_taiga_fontanka_metas',
    'load_taiga_fontanka'
]
