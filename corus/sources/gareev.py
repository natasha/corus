
import re

from ..path import (
    list_dir,
    join_path
)
from ..io import load_lines
from ..meta import Meta
from ..record import Record
from ..token import find_tokens
from ..bio import bio_spans


META = Meta(
    label='gareev',
    title='Gareev',
    source='https://www.researchgate.net/publication/262203599_Introducing_Baselines_for_Russian_Named_Entity_Recognition',
    instruction=[
        'Email Rinat Gareev (gareev-rm@yandex.ru) ask for dataset',
        'tar -xvf rus-ner-news-corpus.iob.tar.gz',
        'rm rus-ner-news-corpus.iob.tar.gz'
    ]
)


class GareevRecord(Record):
    __attributes__ = ['text', 'spans']

    def __init__(self, text, spans):
        self.text = text
        self.spans = spans


def parse_conll(lines):
    chunks = []
    tags = []
    for line in lines:
        chunk, tag = line.split('\t', 1)
        chunks.append(chunk)
        tags.append(tag)
    text = ' '.join(chunks)
    tokens = list(find_tokens(chunks, text))
    spans = list(bio_spans(tokens, tags))
    return GareevRecord(text, spans)


def load_id(id, dir):
    path = join_path(dir, '%s.txt.iob' % id)
    lines = load_lines(path)
    return parse_conll(lines)


def list_ids(dir):
    for filename in list_dir(dir):
        match = re.match(r'^(.+).txt.iob', filename)
        if match:
            yield match.group(1)


def load(dir):
    for id in list_ids(dir):
        yield load_id(id, dir)
