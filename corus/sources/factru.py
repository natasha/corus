
import re
from ..path import (
    list_dir,
    join_path
)
from ..record import Record
from ..meta import Meta
from ..io import (
    load_text,
    load_lines,
)


META = Meta(
    label='factru',
    title='factRuEval-2016',
    source='https://github.com/dialogue-evaluation/factRuEval-2016/',
    description='254 news articles with PER, LOC, ORG markup.',
    instruction=[
        'wget https://github.com/dialogue-evaluation/factRuEval-2016/archive/master.zip',
        'unzip master.zip',
        'rm master.zip'
    ]
)


class FactruSpan(Record):
    __attributes__ = ['id', 'type', 'start', 'stop']

    def __init__(self, id, type, start, stop):
        self.id = id
        self.type = type
        self.start = start
        self.stop = stop


class FactruObject(Record):
    __attributes__ = ['id', 'type', 'spans']

    def __init__(self, id, type, spans):
        self.id = id
        self.type = type
        self.spans = spans


class FactruMarkup(Record):
    __attributes__ = ['id', 'text', 'objects']

    def __init__(self, id, text, objects):
        self.id = id
        self.text = text
        self.objects = objects


def list_ids(dir, set):
    for filename in list_dir(join_path(dir, set)):
        match = re.match(r'^book_(\d+)\.txt$', filename)
        if match:
            yield match.group(1)


def txt_path(id, dir, set):
    return join_path(dir, set, 'book_%s.txt' % id)


def spans_path(id, dir, set):
    return join_path(dir, set, 'book_%s.spans' % id)


def objects_path(id, dir, set):
    return join_path(dir, set, 'book_%s.objects' % id)


def parse_spans(lines):
    for line in lines:
        id, type, start, size, _ = line.split(None, 4)
        start = int(start)
        stop = start + int(size)
        yield FactruSpan(id, type, start, stop)


def parse_objects(lines, spans):
    id_spans = {_.id: _ for _ in spans}
    for line in lines:
        parts = iter(line.split())
        id = next(parts)
        type = next(parts)
        spans = []
        for index in parts:
            if not index.isdigit():
                break
            span = id_spans[index]
            spans.append(span)
        yield FactruObject(id, type, spans)


def load_id(id, dir, set):
    path = txt_path(id, dir, set)
    text = load_text(path)
    path = spans_path(id, dir, set)
    lines = load_lines(path)
    spans = list(parse_spans(lines))
    path = objects_path(id, dir, set)
    lines = load_lines(path)
    objects = list(parse_objects(lines, spans))
    return FactruMarkup(id, text, objects)


def load(dir, sets=['devset', 'testset']):
    for set in sets:
        for id in list_ids(dir, set):
            yield load_id(id, dir, set)
