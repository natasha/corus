# coding: utf8

import re
from datetime import datetime
from os import walk as walk_
from os.path import (
    split as split_path,
    splitext as split_ext,
    join as join_path
)

from corus.record import Record
from corus.io import (
    load_text,
    load_lines
)


RU = 'ru'
BG = 'bg'
CS = 'cs'
PL = 'pl'
LANGS = [RU, BG, CS, PL]

ANNOTATED = 'annotated'
RAW = 'raw'

TXT = '.txt'
OUT = '.out'


class BsnlpId(Record):
    __attributes__ = ['lang', 'type', 'name', 'path']

    def __init__(self, lang, type, name, path):
        self.lang = lang
        self.type = type
        self.name = name
        self.path = path


class BsnlpRaw(Record):
    __attributes__ = ['id', 'name', 'lang', 'date', 'url', 'text']

    def __init__(self, id, name, lang, date, url, text):
        self.id = id
        self.name = name
        self.lang = lang
        self.date = date
        self.url = url
        self.text = text


class BsnlpAnnotated(Record):
    __attributes__ = ['id', 'name', 'substrings']

    def __init__(self, id, name, substrings):
        self.id = id
        self.name = name
        self.substrings = substrings


class BsnlpSubstring(Record):
    __attributes__ = ['text', 'normal', 'type', 'id']

    def __init__(self, text, normal, type, id):
        self.text = text
        self.normal = normal
        self.type = type
        self.id = id


class BsnlpSpan(Record):
    __attributes__ = ['start', 'stop', 'type', 'normal', 'id']

    def __init__(self, start, stop, type, normal, id):
        self.start = start
        self.stop = stop
        self.type = type
        self.normal = normal
        self.id = id


class BsnlpMarkup(Record):
    __attributes__ = ['id', 'name', 'lang', 'date', 'url', 'text', 'substrings']

    def __init__(self, id, name, lang, date, url, text, substrings):
        self.id = id
        self.name = name
        self.lang = lang
        self.date = date
        self.url = url
        self.text = text
        self.substrings = substrings

    @property
    def spans(self):
        spans = find_spans(self.text, self.substrings)
        return filter_overlapping(spans)


def walk(dir):
    def onerror(error):
        raise error

    return walk_(dir, onerror=onerror)


def load_ids(dir, langs):
    if not langs:
        langs = LANGS

    # root bsnlp/sample_pl_cs_ru_bg/raw/cs
    # filename brexit_cs.txt_file_100.txt
    for root, subdirs, filenames in walk(dir):
        tail, lang = split_path(root)
        if lang not in langs:
            continue

        tail, type = split_path(tail)
        if type not in (ANNOTATED, RAW):
            # raw/nord_stream/ru/nord_stream_ru.txt_file_44.txt
            tail, type = split_path(tail)
        assert type in (ANNOTATED, RAW), root

        for filename in filenames:
            name, ext = split_ext(filename)
            if ext not in (TXT, OUT):
                continue
            path = join_path(root, filename)
            yield BsnlpId(lang, type, name, path)


def select_type(ids, type):
    for id in ids:
        if id.type == type:
            yield id


RAW_PATTERN = re.compile(r'''
^([^\n]+)\n
(ru|bg|cs|pl)\n
(\d\d\d\d-\d\d-\d\d)\n
(https?://[^\n]+)?\n
''', re.X)


def parse_raw(name, text):
    match = RAW_PATTERN.search(text)
    assert match, text

    id, lang, date, url = match.groups()
    date = datetime.strptime(date, '%Y-%m-%d')
    text = text[match.end():]
    return BsnlpRaw(id, name, lang, date, url, text)


def load_raw(records):
    for record in records:
        text = load_text(record.path)
        yield parse_raw(record.name, text)


# Евросоюза		ORG	ORG-European-Union
ANNOTATED_PATTERN = re.compile(r'''
^([^\t]+)
\t([^\t]+)?
\t([^\t]+)
\t?([^\t]+)?$
''', re.X)


def parse_substrings(lines):
    for line in lines:
        match = ANNOTATED_PATTERN.match(line)
        if not match:
            # single case
            # ЕНП	ЕНП	ORG	ORG-EPP ЕС	ЕС	ORG	ORG-European-Union
            continue
        text, normal, type, id = match.groups()
        yield BsnlpSubstring(text, normal, type, id)


def parse_annotated(name, lines):
    id = next(lines).lstrip('\ufeff')
    substrings = list(parse_substrings(lines))
    return BsnlpAnnotated(id, name, substrings)


def load_annotated(records):
    for record in records:
        lines = load_lines(record.path)
        yield parse_annotated(record.name, lines)


def merge(raw, annotated):
    id_raw = {_.name: _ for _ in raw}
    for record in annotated:
        raw = id_raw[record.name]
        yield BsnlpMarkup(
            raw.id, raw.name, raw.lang, raw.date, raw.url,
            raw.text, record.substrings
        )


def load_bsnlp(dir, langs=[RU]):
    ids = list(load_ids(dir, langs))
    raw = load_raw(select_type(ids, RAW))
    annotated = load_annotated(select_type(ids, ANNOTATED))
    return merge(raw, annotated)


############
#
#     SPANS
#
#########


def iter_find(text, substring):
    start = text.find(substring)
    if start < 0:
        # For ru just 3 substrings missing:
        #   "Северный поток – 2"
        #   Евгений Хвостик
        #   Тереза Мэй
        return

    while start >= 0:
        stop = start + len(substring)
        yield start, stop
        start = text.find(substring, stop)


def find_spans(text, substrings):
    for substring in substrings:
        for start, stop in iter_find(text, substring.text):
            yield BsnlpSpan(
                start, stop,
                substring.type, substring.normal, substring.id
            )


def filter_overlapping(spans):
    previous = None
    spans = sorted(spans, key=lambda _: (_.start, -_.stop))
    for span in spans:
        if previous and previous.stop > span.start:
            continue
        yield span
        previous = span
