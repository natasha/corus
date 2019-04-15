
from ..record import Record
from ..meta import Meta
from ..io import (
    load_gz_lines,
    parse_csv
)


META = Meta(
    label='lenta',
    title='Lenta.ru',
    source='https://github.com/yutkin/Lenta.Ru-News-Dataset',
    description='Dump of lenta.ru, ~790 000 articles, ~1.9Gb of text.',
    instruction=[
        'wget https://github.com/yutkin/Lenta.Ru-News-Dataset/releases/download/v1.0/lenta-ru-news.csv.gz'
    ]
)


class LentaRecord(Record):
    __attributes__ = ['url', 'title', 'text', 'topic', 'tags']

    def __init__(self, url, title, text, topic, tags):
        self.url = url
        self.title = title
        self.text = text
        self.topic = topic
        self.tags = tags


def parse(lines):
    rows = parse_csv(lines)
    for cells in rows:
        yield LentaRecord(*cells)


def load(path):
    lines = load_gz_lines(path)
    return parse(lines)
