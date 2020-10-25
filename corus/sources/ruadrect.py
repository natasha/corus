from corus.record import Record
from corus.io import (
    parse_tsv,
    skip_header,
    rstrip
)

# – id: уникальный номер сообщения в системе twitter;
# – text:  текст сообщения (твита);
# - label: класс твита, 1 - содержит упоминание побочного эффекта, 0 - не содердит


class RuADReCTRecord(Record):
    __attributes__ = ['tweet_id', 'text', 'label']

    def __init__(self, tweet_id, text, label):
        self.tweet_id = tweet_id
        self.text = text
        self.label = label


def parse_ruadrect(lines):
    rows = parse_tsv(lines)
    skip_header(rows)
    for cells in rows:
        yield RuADReCTRecord(*cells)


def load_lines(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            yield rstrip(line)


def load_ruadrect(path):
    lines = load_lines(path)
    return parse_ruadrect(lines)
