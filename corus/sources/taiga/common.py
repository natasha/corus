
from io import TextIOWrapper
from itertools import islice as head
import tarfile

from corus.record import Record
from corus.path import (
    get_filename,
    split_ext
)
from corus.zip import (
    open_zip,
    read_zip_header,
    read_zip_data
)
from corus.io import (
    match_names,

    parse_tsv,
    skip_header,
)
from corus.compat import patch_tar_file


class ArchiveRecord(Record):
    __attributes__ = ['name', 'offset', 'file']

    def __init__(self, name, offset, file):
        self.name = name
        self.offset = offset
        self.file = file


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


def load_tar(path, offset=0):
    with tarfile.open(path) as tar:
        tar.fileobj.seek(offset)
        while True:
            member = tarfile.TarInfo.fromtarfile(tar)
            if not member.isfile():
                continue

            file = tar.extractfile(member)
            patch_tar_file(file)
            yield ArchiveRecord(
                name=member.name,
                offset=member.offset,
                file=file
            )

            tar.members = []
            tar.fileobj.seek(tar.offset)


def load_zip(path, offset=0):
    with open_zip(path) as zip:
        zip.seek(offset)
        while True:
            offset = zip.tell()

            header = read_zip_header(zip)
            if not header:
                break
            if not header.uncompressed:
                continue

            file = read_zip_data(zip, header)
            yield ArchiveRecord(
                name=header.name,
                offset=offset,
                file=file
            )


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
