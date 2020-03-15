
import re

from corus.path import (
    list_dir,
    join_path
)
from corus.io import load_lines
from corus.record import Record


class GareevToken(Record):
    __attributes__ = ['text', 'tag']

    def __init__(self, text, tag):
        self.text = text
        self.tag = tag


class GareevRecord(Record):
    __attributes__ = ['tokens']

    def __init__(self, tokens):
        self.tokens = tokens


def parse_conll(lines):
    for line in lines:
        text, tag = line.split('\t', 1)
        yield GareevToken(text, tag)


def parse_gareev(lines):
    tokens = list(parse_conll(lines))
    return GareevRecord(tokens)


def load_id(id, dir):
    path = join_path(dir, '%s.txt.iob' % id)
    lines = load_lines(path)
    return parse_gareev(lines)


def list_ids(dir):
    for filename in list_dir(dir):
        match = re.match(r'^(.+).txt.iob', filename)
        if match:
            yield match.group(1)


def load_gareev(dir):
    for id in list_ids(dir):
        yield load_id(id, dir)
