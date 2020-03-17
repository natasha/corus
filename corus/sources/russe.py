
from corus.record import Record
from corus.io import (
    load_lines,
    parse_csv,
    dict_csv
)


class RusseSemRecord(Record):
    __attributes__ = ['word1', 'word2', 'sim']

    def __init__(self, word1, word2, sim):
        self.word1 = word1
        self.word2 = word2
        self.sim = sim


# word1,word2,related,sim
# автомат,калашникова,assoc,1
# автомат,пулемет,assoc,1
# автомат,пистолет,assoc,1
# автомат,война,assoc,1
# автомат,газ. вода,assoc,1
# автомат,год,random,0
# автомат,человек,random,0
# автомат,время,random,0
# автомат,район,random,0


def parse_russe(lines):
    records = parse_csv(lines)
    items = dict_csv(records)
    for item in items:
        word1 = item['word1']
        word2 = item['word2']
        sim = float(item['sim'])
        yield RusseSemRecord(word1, word2, sim)


def load_russe(path):
    lines = load_lines(path)
    return parse_russe(lines)


def load_russe_hj(path):
    return load_russe(path)


def load_russe_rt(path):
    return load_russe(path)


def load_russe_ae(path):
    return load_russe(path)


__all__ = [
    'load_russe_hj',
    'load_russe_rt',
    'load_russe_ae',
]
