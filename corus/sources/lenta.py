
from corus.record import Record
from corus.io import (
    load_gz_lines,
    parse_csv,
    skip_header
)


class LentaRecord(Record):
    __attributes__ = ['url', 'title', 'text', 'topic', 'tags']

    def __init__(self, url, title, text, topic, tags):
        self.url = url
        self.title = title
        self.text = text
        self.topic = topic
        self.tags = tags


def parse_lenta(lines):
    rows = parse_csv(lines)
    skip_header(rows)
    for cells in rows:
        yield LentaRecord(*cells)


def load_lenta(path):
    lines = load_gz_lines(path)
    return parse_lenta(lines)
