
from corus.record import Record
from corus.io import (
    load_lines,
    parse_tsv,
    skip_header
)


class SimlexRecord(Record):
    __attributes__ = ['word1', 'word2', 'score']

    def __init__(self, word1, word2, score):
        self.word1 = word1
        self.word2 = word2
        self.score = score


def parse_simlex(lines):
    skip_header(lines)
    records = parse_tsv(lines)
    for word1, word2, score in records:
        score = float(score)
        yield SimlexRecord(word1, word2, score)


def load_simlex(path):
    lines = load_lines(path)
    return parse_simlex(lines)
