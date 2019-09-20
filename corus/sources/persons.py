
import re
from corus.record import Record
from corus.io import (
    list_zip,
    load_zip_texts,
    parse_xml,
)


TEXT = 'text.txt'
ANNO = 'anno.markup.xml'


class PersonsSpan(Record):
    __attributes__ = ['id', 'start', 'stop', 'value']

    def __init__(self, id, start, stop, value):
        self.id = id
        self.start = start
        self.stop = stop
        self.value = value


class PersonsMarkup(Record):
    __attributes__ = ['text', 'spans']

    def __init__(self, text, spans):
        self.text = text
        self.spans = spans


def list_ids(path):
    for name in list_zip(path):
        match = re.match(r'^Persons-1000/collection/([^/]+)/text\.txt$', name)
        if match:
            yield match.group(1)


def part_names(ids, part):
    for id in ids:
        yield 'Persons-1000/collection/%s/%s' % (id, part)


def parse_anno(text):
    xml = parse_xml(text)
    for entry in xml.findall('entry'):
        id = int(entry.find('id').text)
        start = int(entry.find('offset').text)
        size = int(entry.find('length').text)
        stop = start + size
        attribute = entry.find('attribute')
        value = attribute.find('value').text
        yield PersonsSpan(id, start, stop, value)


def load_ids(ids, path):
    names = part_names(ids, TEXT)
    texts = load_zip_texts(path, names, 'cp1251')

    names = part_names(ids, ANNO)
    annos = load_zip_texts(path, names, 'utf-8')
    for text, anno in zip(texts, annos):
        spans = list(parse_anno(anno))
        yield PersonsMarkup(text, spans)


def load_persons(path):
    ids = list(list_ids(path))
    return load_ids(ids, path)
