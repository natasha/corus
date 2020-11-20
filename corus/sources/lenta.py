
from datetime import datetime

from corus.record import Record
from corus.io import (
    load_gz_lines,
    load_bz2_lines,
    parse_csv,
    skip_header
)


class LentaRecord(Record):
    __attributes__ = ['url', 'title', 'text', 'topic', 'tags', 'date']

    def __init__(self, url, title, text, topic, tags, date=None):
        self.url = url
        self.title = title
        self.text = text
        self.topic = topic
        self.tags = tags
        self.date = date


def parse_lenta(lines):
    rows = parse_csv(lines)
    skip_header(rows)
    for cells in rows:
        yield LentaRecord(*cells)


def parse_lenta2(lines):
    for record in parse_lenta(lines):
        record.date = datetime.strptime(record.date, '%Y/%m/%d')
        yield record


def load_lenta(path):
    lines = load_gz_lines(path)
    return parse_lenta(lines)


def load_lenta2(path):
    lines = load_bz2_lines(path)
    return parse_lenta2(lines)
