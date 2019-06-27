
import tarfile
from io import TextIOWrapper
from datetime import datetime

from corus.record import Record
from corus.io import (
    parse_csv,
    skip_header,
)
from corus.compat import patch_tar_file


class BuriyRecord(Record):
    __attributes__ = ['timestamp', 'url', 'edition', 'topics', 'title', 'text']

    def __init__(self, timestamp, url, edition, topics, title, text):
        self.timestamp = timestamp
        self.url = url
        self.edition = edition
        self.topics = topics
        self.title = title
        self.text = text


def load_tar(path, encoding='utf8'):
    with tarfile.open(path) as tar:
        for member in tar:
            if not member.isfile():
                continue
            file = tar.extractfile(member)
            patch_tar_file(file)
            yield TextIOWrapper(file, encoding)


def parse_timestamp(timestamp):
    for pattern in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
        try:
            return datetime.strptime(timestamp, pattern)
        except ValueError:
            continue


def maybe_none(value, none=('',)):
    if value in none:
        return
    return value


def parse_buriy(lines, max_text=10000000):
    rows = parse_csv(lines, max_field=max_text)
    skip_header(rows)
    for row in rows:
        timestamp, url, edition, topics, title, text = row
        timestamp = parse_timestamp(timestamp)
        edition = maybe_none(edition, ('', '-'))
        topics = maybe_none(topics)
        yield BuriyRecord(
            timestamp=timestamp,
            url=url,
            edition=edition,
            topics=topics,
            title=title,
            text=text
        )


def load_buriy(path):
    for lines in load_tar(path):
        for record in parse_buriy(lines):
            yield record


def load_buriy_lenta(path):
    return load_buriy(path)


def load_buriy_news(path):
    return load_buriy(path)


def load_buriy_webhose(path):
    return load_buriy(path)


__all__ = [
    'load_buriy_lenta',
    'load_buriy_news',
    'load_buriy_webhose'
]
