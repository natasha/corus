# coding: utf8

from datetime import datetime

from corus.record import Record
from corus.io import (
    list_zip,
    load_zip_lines,
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


def none_row(row, nones=('-', '')):
    for cell in row:
        if cell in nones:
            cell = None
        yield cell


def maybe_int(value):
    if value:
        return int(value)
    return


def fix_csv(lines):
    # https://github.com/ods-ai-ml4sg/proj_news_viz/blob/master/scraping/newsbot/newsbot/pipelines.py#L36
    for line in lines:
        yield line.replace(r'\"', '""')


def fix_new_line(text):
    if text:
        return text.replace(r'\n', '\n')


def parse_news(lines):
    rows = parse_csv(fix_csv(lines))
    header = skip_header(rows)
    for row in rows:
        row = list(none_row(row))
        if len(row) != len(header) + 1:  # extra , before EOL
            # rare Д.Акулинин, а также М.Кузовлев.\n\",-,-,-,-,-,-,-,-,-
            continue

        (timestamp, url, edition, topics, authors, title, text,
         fb, vk, ok, twitter, lj, tg, likes, views, comments, _) = row
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
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
        if authors:
            authors = authors.split(',')
        yield NewsRecord(
            timestamp, url,
            fix_new_line(edition),
            fix_new_line(topics),
            authors,
            fix_new_line(title),
            fix_new_line(text),
            stats
        )


def load_lines(path):
    for name in list_zip(path):
        for line in load_zip_lines(path, name):
            yield line


def load_news(path):
    lines = load_lines(path)
    return parse_news(lines)


def load_ods_interfax(path):
    return load_news(path)


def load_ods_gazeta(path):
    return load_news(path)


__all__ = [
    'load_ods_interfax',
    'load_ods_gazeta'
]
