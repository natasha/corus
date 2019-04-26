
from io import TextIOWrapper
from itertools import islice as head

from ...record import Record
from ...path import (
    get_filename,
    split_ext
)
from ...io import (
    match_names,

    parse_tsv,
    skip_header,

    load_tar,
    load_zip
)


class TaigaRecord(Record):
    __attributes__ = ['id', 'meta', 'text']

    def __init__(self, id, meta, text):
        self.id = id
        self.meta = meta
        self.text = text


class Author(Record):
    __attributes__ = ['name', 'readers', 'texts', 'profession', 'about', 'url']

    def __init__(self, name, readers=None, texts=None,
                 profession=None, about=None, url=None):
        self.name = name
        self.readers = readers
        self.texts = texts
        self.profession = profession
        self.about = about
        self.url = url


class Meta(Record):
    __attributes__ = ['id', 'timestamp', 'tags',
                      'themes', 'rubric', 'genre', 'topic',
                      'author', 'lang', 'title', 'url']

    def __init__(self, id, timestamp=None, tags=None,
                 themes=None, rubric=None, genre=None, topic=None,
                 author=None, lang=None, title=None, url=None):
        self.id = id
        self.timestamp = timestamp
        self.tags = tags
        self.themes = themes
        self.rubric = rubric
        self.genre = genre
        self.topic = topic
        self.author = author
        self.lang = lang
        self.title = title
        self.url = url


def parse_meta(file, encoding='utf8'):
    lines = TextIOWrapper(file, encoding)
    rows = parse_tsv(lines)
    header = skip_header(rows)
    for row in rows:
        yield dict(zip(header, row))


def load_metas(path, pattern, offset, count, load):
    records = load(path, offset)
    records = match_names(records, pattern)
    records = head(records, count)
    for record in records:
        for item in parse_meta(record.file):
            yield item


def load_tar_metas(path, pattern, offset, count):
    return load_metas(path, pattern, offset, count, load_tar)


def load_zip_metas(path, pattern, offset, count):
    return load_metas(path, pattern, offset, count, load_zip)


def load_texts(path, pattern, offset, count, parse_id, load, encoding='utf8'):
    records = load(path, offset=offset)
    records = match_names(records, pattern)
    records = head(records, count)
    for record in records:
        id = parse_id(record.name)
        file = TextIOWrapper(record.file, encoding)
        text = file.read()
        yield TaigaRecord(
            id=id,
            meta=None,
            text=text
        )


def parse_filename_id(path):
    id, _ = split_ext(get_filename(path))
    return id


def load_tar_texts(path, pattern, offset, count, parse_id=parse_filename_id):
    return load_texts(path, pattern, offset, count, parse_id, load_tar)


def load_zip_texts(path, pattern, offset, count, parse_id=parse_filename_id):
    return load_texts(path, pattern, offset, count, parse_id, load_zip)


def merge_metas(records, metas=None):
    if not metas:
        for record in records:
            yield record
    else:
        metas = {_.id: _ for _ in metas}
        for record in records:
            record.meta = metas.get(record.id)
            yield record


def patch_month(date, months):
    for source, target in months.items():
        if source in date:
            return date.replace(source, target)
