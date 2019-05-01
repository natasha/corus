
import re

from corus.path import (
    list_dir,
    join_path
)
from corus.io import load_lines
from corus.record import Record
from corus.token import find_tokens
from corus.bio import bio_spans


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


def load_gareev(dir):
    for id in list_ids(dir):
        yield load_id(id, dir)
