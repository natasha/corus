
from io import StringIO
import json

from corus.record import Record
from corus.io import load_bz2_lines
from corus.third.WikiExtractor import (
    options,
    pages_from,
    Extractor
)


options.write_json = True


class WikiRecord(Record):
    __attributes__ = ['id', 'url', 'title', 'text']

    def __init__(self, id, url, title, text):
        self.id = id
        self.url = url
        self.title = title
        self.text = text

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data['id'],
            url=data['url'],
            title=data['title'],
            text=data['text']
        )


class Extractor_(Extractor):
    def extract_(self):
        output = StringIO()
        self.extract(output)
        return json.loads(output.getvalue())


def load_wiki(path):
    lines = load_bz2_lines(path)
    records = pages_from(lines)
    for record in records:
        id, revision, title, _, _, page = record
        extractor = Extractor_(id, revision, title, page)
        data = extractor.extract_()
        yield WikiRecord.from_json(data)
