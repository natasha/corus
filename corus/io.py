
import gzip
import bz2
import tarfile

import csv
import json

import xml.etree.ElementTree as ET

from fnmatch import fnmatch as match_pattern


def load_text(path):
    with open(path) as file:
        return file.read()


def dump_text(text, path):
    with open(path, 'w') as file:
        file.write(text)


def load_lines(path):
    with open(path) as file:
        for line in file:
            yield line.rstrip('\n')


def parse_xml(content):
    return ET.fromstring(content)


def load_gz_lines(path, encoding='utf8', gzip=gzip):
    with gzip.open(path, mode='rt', encoding=encoding) as file:
        for line in file:
            yield line.rstrip()


def load_bz2_lines(path, encoding='utf8'):
    return load_gz_lines(path, encoding=encoding, gzip=bz2)


def parse_csv(lines, delimiter=','):
    return csv.reader(lines, delimiter=delimiter)


def parse_tsv(lines):
    return parse_csv(lines, delimiter='\t')


def skip_header(rows):
    return next(rows)


def parse_jsonl(lines):
    for line in lines:
        yield json.loads(line)


def open_tar(path):
    return tarfile.open(path)


def list_tar(tar):
    for member in tar:
        yield member
        tar.members = []


def match_names(records, pattern):
    for record in records:
        if match_pattern(record.name, pattern):
            yield record

class ZipRecord(Record):
    __attributes__ = ['name', 'offset', 'file']

    def __init__(self, name, offset, file):
        self.name = name
        self.offset = offset
        self.file = file


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
            yield ZipRecord(
                name=header.name,
                offset=offset,
                file=file
            )
