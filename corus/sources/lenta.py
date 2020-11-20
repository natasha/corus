
from corus.record import Record
from corus.io import (
    load_gz_lines,
    load_bz2_lines,
    parse_csv,
    skip_header
)


class LentaRecord(Record):
    """
    Class for Lenta.Ru Dataset v1.0
    """
    __attributes__ = ['url', 'title', 'text', 'topic', 'tags']

    def __init__(self, url, title, text, topic, tags):
        self.url = url
        self.title = title
        self.text = text
        self.topic = topic
        self.tags = tags


class LentaRecord2(Record):
    """
    Class for Lenta.Ru Dataset v1.1
    """
    __attributes__ = ['url', 'title', 'text', 'topic', 'tags', 'date']

    def __init__(self, url, title, text, topic, tags, date):
        self.url = url
        self.title = title
        self.text = text
        self.topic = topic
        self.tags = tags
        self.date = date


def parse_lenta_(lines, lenta_class):
    rows = parse_csv(lines)
    skip_header(rows)
    for cells in rows:
        yield lenta_class(*cells)


def parse_lenta(lines):
    return parse_lenta_(lines, LentaRecord)


def parse_lenta2(lines):
    return parse_lenta_(lines, LentaRecord2)


def load_lenta(path):
    """
    loads Lenta.Ru Dataset v1.0
    """
    lines = load_gz_lines(path)
    return parse_lenta(lines)


def load_lenta2(path):
    """
    loads Lenta.Ru Dataset v1.1
    """
    lines = load_bz2_lines(path)
    return parse_lenta2(lines)
