# coding: utf8

from datetime import datetime

from corus.record import Record
from corus.io import (
    load_gz_lines,
    parse_csv,
    skip_header
)


class NewsRecord(Record):
    __attributes__ = [
        'timestamp', 'url', 'edition', 'topics',
        'authors', 'title', 'text', 'stats'
    ]

    def __init__(self, timestamp, url, edition, topics, authors, title, text, stats):
        self.timestamp = timestamp
        self.url = url
        self.edition = edition
        self.topics = topics
        self.authors = authors
        self.title = title
        self.text = text
        self.stats = stats


class Stats(Record):
    __attributes__ = [
        'fb', 'vk', 'ok', 'twitter', 'lj', 'tg',
        'likes', 'views', 'comments'
    ]

    def __init__(self, fb, vk, ok, twitter, lj, tg, likes, views, comments):
        self.fb = fb
        self.vk = vk
        self.ok = ok
        self.twitter = twitter
        self.lj = lj
        self.tg = tg
        self.likes = likes
        self.views = views
        self.comments = comments


def none_row(row):
    for cell in row:
        if not cell or cell == '-':
            cell = None
        yield cell


def maybe_int(value):
    if value:
        return int(value)
    return


def parse_news(lines):
    # tass raises "field larger than field limit"
    rows = parse_csv(lines, max_field=100000000)
    skip_header(rows)
    for row in rows:
        (timestamp, url, edition, topics, authors, title, text,
         fb, vk, ok, twitter, lj, tg, likes, views, comments) = none_row(row)

        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

        if authors:
            authors = authors.split(',')

        # empty texts in meduza
        text = text or ''

        stats = Stats(
            maybe_int(fb),
            maybe_int(vk),
            maybe_int(ok),
            maybe_int(twitter),
            maybe_int(lj),
            maybe_int(tg),
            maybe_int(likes),
            maybe_int(views),
            maybe_int(comments)
        )
        yield NewsRecord(
            timestamp, url, edition, topics, authors,
            title, text, stats
        )


def load_news(path):
    lines = load_gz_lines(path)
    return parse_news(lines)


def load_ods_interfax(path):
    return load_news(path)


def load_ods_gazeta(path):
    return load_news(path)


def load_ods_izvestia(path):
    return load_news(path)


def load_ods_meduza(path):
    return load_news(path)


def load_ods_ria(path):
    return load_news(path)


def load_ods_rt(path):
    return load_news(path)


def load_ods_tass(path):
    return load_news(path)


__all__ = [
    'load_ods_interfax',
    'load_ods_gazeta',
    'load_ods_izvestia',
    'load_ods_meduza',
    'load_ods_ria',
    'load_ods_rt',
    'load_ods_tass',
]
