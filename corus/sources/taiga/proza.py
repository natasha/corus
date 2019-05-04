# coding: utf8

from datetime import datetime

from .common import (
    Author,
    Meta,
    load_zip_metas,
    load_zip_texts,
    merge_metas
)


# {'URL': 'http://www.stihi.ru/2015/12/31/9302',
#   'author': 'Макс Майер-Младший',
#   'author_readers': '26',
#   'author_texts': '2085',
#   'authorlink': 'http://www.stihi.ru/avtor/380979994453',
#   'date': '31.12.2015',
#   'genre': 'лирика',
#   'path': '/home/tsha/stihi_ru/texts/2015/12/20151231001.txt',
#   'textid': '20151231001',
#   'time': '23:56',
#   'title': 'Ти знов являЕшся менi у снi',
#   'topic': 'любовная лирика'}


def parse_metas(items):
    for item in items:
        id = item['textid']

        timestamp = item['date'] + item['time']
        timestamp = datetime.strptime(timestamp, '%d.%m.%Y%H:%M')

        name = item['author']
        readers = item['author_readers'] or None
        if readers:
            readers = int(readers)
        texts = item['author_texts'] or None
        if texts:
            texts = int(texts)
        url = item['authorlink']
        author = Author(
            name=name,
            readers=readers,
            texts=texts,
            url=url
        )

        genre = item['genre']
        topic = item['topic']
        title = item['title']
        url = item['URL']
        yield Meta(
            id=id,
            timestamp=timestamp,
            author=author,
            genre=genre,
            topic=topic,
            title=title,
            url=url
        )


def load_taiga_proza_metas(path, offset=0, count=2017 - 2005 + 1):
    items = load_zip_metas(path, '*/metatable_texts.txt', offset, count)
    return parse_metas(items)


def load_taiga_stihi_metas(path, offset=0, count=2017 - 2015 + 1):
    items = load_zip_metas(path, '*/metatable_texts.txt', offset, count)
    return parse_metas(items)


# proza_ru/home/tsha/proza_ru/tagged_texts/2015/12/20151231005.txt
# proza_ru/home/tsha/proza_ru/texts/2015/12/20151231005.txt


def load_taiga_proza(path, metas=None, offset=51432715409, count=1732589):
    records = load_zip_texts(path, '*/texts/*.txt', offset, count)
    return merge_metas(records, metas)


def load_taiga_stihi(path, metas=None, offset=22304202421, count=9157973):
    records = load_zip_texts(path, '*/texts/*.txt', offset, count)
    return merge_metas(records, metas)


__all__ = [
    'load_taiga_proza_metas',
    'load_taiga_proza',
    'load_taiga_stihi_metas',
    'load_taiga_stihi',
]
