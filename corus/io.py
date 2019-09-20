
import gzip
import bz2
from zipfile import ZipFile

import csv
import json

import xml.etree.ElementTree as ET

from fnmatch import fnmatch as match_pattern

from .compat import PY2


UTF8 = 'utf8'
CP1251 = 'cp1251'


#######
#
#   UTILS
#
#######


def match_names(records, pattern):
    for record in records:
        if match_pattern(record.name, pattern):
            yield record


#######
#
#    TEXT
#
########


if PY2:
    def load_text(path, encoding=UTF8):
        with open(path) as file:
            return file.read().decode(encoding)

    def dump_text(text, path, encoding=UTF8):
        with open(path, 'w') as file:
            file.write(text.encode(encoding))

    def load_lines(path, encoding=UTF8):
        with open(path) as file:
            for line in file:
                yield line.decode(UTF8).rstrip()


else:
    def load_text(path):
        with open(path) as file:
            return file.read()

    def dump_text(text, path):
        with open(path, 'w') as file:
            file.write(text)

    def load_lines(path):
        with open(path) as file:
            for line in file:
                yield line.rstrip()


#####
#
#   XML
#
######


def parse_xml(content):
    return ET.fromstring(content)


#########
#
#   GZ
#
#####


if PY2:
    def load_gz_lines(path, encoding=UTF8):
        with gzip.open(path) as file:
            for line in file:
                yield line.decode(encoding).rstrip()

else:
    def load_gz_lines(path, encoding=UTF8):
        with gzip.open(path, mode='rt', encoding=encoding) as file:
            for line in file:
                yield line.rstrip()


########
#
#    BZ
#
########


if PY2:
    def load_bz2_lines(path, encoding=UTF8):
        with bz2.BZ2File(path) as file:
            for line in file:
                yield line.decode(encoding).rstrip()

else:
    def load_bz2_lines(path, encoding=UTF8):
        with bz2.open(path, mode='rt', encoding=encoding) as file:
            for line in file:
                yield line.rstrip()


#######
#
#   ZIP
#
########


def list_zip(path):
    with ZipFile(path) as zip:
        return zip.namelist()


def load_zip_lines(path, name, encoding=UTF8):
    with ZipFile(path) as zip:
        with zip.open(name) as file:
            for line in file:
                yield line.decode(encoding).rstrip()


def load_zip_texts(path, names, encoding):
    with ZipFile(path) as zip:
        for name in names:
            with zip.open(name) as file:
                yield file.read().decode(encoding)


########
#
#   CSV
#
#######


if PY2:
    def encode(items, encoding=UTF8):
        for item in items:
            yield item.encode(encoding)

    def decode(items, encoding=UTF8):
        for item in items:
            yield item.decode(encoding)

    def parse_csv(lines, delimiter=',', max_field=None, encoding=UTF8):
        if max_field:
            csv.field_size_limit(max_field)
        lines = encode(lines, encoding)
        rows = csv.reader(lines, delimiter=delimiter)
        for row in rows:
            yield list(decode(row, encoding))

else:
    def parse_csv(lines, delimiter=',', max_field=None):
        if max_field:
            csv.field_size_limit(max_field)
        return csv.reader(lines, delimiter=delimiter)


def parse_tsv(lines):
    return parse_csv(lines, delimiter='\t')


def skip_header(rows):
    return next(rows)


#########
#
#    JSONL
#
#######


def parse_jsonl(lines):
    for line in lines:
        yield json.loads(line)
