# coding: utf8
from __future__ import unicode_literals

import re

from corus.record import Record
from corus.io import (
    load_gz_lines,
    parse_jsonl
)


class RiaRawRecord(Record):
    __attributes__ = ['title', 'text']

    def __init__(self, title, text):
        self.title = title
        self.text = text


class RiaRecord(Record):
    __attributes__ = ['title', 'prefix', 'text']

    def __init__(self, title, prefix, text):
        self.title = title
        self.prefix = prefix
        self.text = text


def parse_ria_raw(lines):
    records = parse_jsonl(lines)
    for record in records:
        yield RiaRawRecord(
            record['title'],
            record['text']
        )


def load_ria_raw(path):
    lines = load_gz_lines(path)
    return parse_ria_raw(lines)


def untag(text):
    return re.sub(r'<[^>]+>', '', text)


def unescape(text):
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&ndash;', '-')
    text = text.replace('&nbsp;', ' ')
    return text


def first_sent(text):
    # москва, 31 янв - риа новости.
    # фарнборо (великобритания), 21 июл - риа новости, александр смотров.
    index = text.find('. ')  # len('. ')
    if index > 0:
        index += 2
        sent, suffix = text[:index], text[index:]
        if 'риа новости' in sent and len(sent) < 70:
            sent = sent.strip()
            return sent, suffix
    return None, text


def parse_ria(records):
    for record in records:
        text = record.text
        text = untag(text)
        text = unescape(text)
        prefix, text = first_sent(text)
        yield RiaRecord(
            record.title,
            prefix,
            text
        )


def load_ria(path):
    records = load_ria_raw(path)
    return parse_ria(records)


__all__ = [
    'load_ria_raw',
    'load_ria'
]
