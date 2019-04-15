
import re

from ..path import (
    list_dir,
    join_path
)
from ..meta import Meta
from ..record import Record
from ..io import load_lines


META = Meta(
    label='ne5',
    title='Collection5',
    source='http://www.labinform.ru/pub/named_entities/',
    instruction=[
        'wget http://www.labinform.ru/pub/named_entities/collection5.zip',
        'unzip collection5.zip',
        'rm collection5.zip'
    ]
)


class Ne5Span(Record):
    __attributes__ = ['index', 'type', 'start', 'stop', 'text']

    def __init__(self, index, type, start, stop, text):
        self.index = index
        self.type = type
        self.start = start
        self.stop = stop
        self.text = text


class Ne5Markup(Record):
    __attributes__ = ['id', 'text', 'spans']

    def __init__(self, id, text, spans):
        self.id = id
        self.text = text
        self.spans = spans


def list_ids(dir):
    for filename in list_dir(dir):
        match = re.match(r'^(.+).txt$', filename)
        if match:
            yield match.group(1)


def txt_path(id, dir):
    return join_path(dir, '%s.txt' % id)


def ann_path(id, dir):
    return join_path(dir, '%s.ann' % id)


def parse_spans(lines):
    # brat format http://brat.nlplab.org/standoff.html
    for line in lines:
        index, type, start, stop, text = line.split(None, 4)
        start = int(start)
        stop = int(stop)
        yield Ne5Span(index, type, start, stop, text)


def load_text(path):
    # do not convert \r\n to \n
    with open(path, newline='') as file:
        return file.read()


def load_id(id, dir):
    path = txt_path(id, dir)
    text = load_text(path)
    path = ann_path(id, dir)
    lines = load_lines(path)
    spans = list(parse_spans(lines))
    return Ne5Markup(id, text, spans)


def load(dir):
    for id in list_ids(dir):
        yield load_id(id, dir)
