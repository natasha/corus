
import gzip
import bz2
from zipfile import ZipFile

import csv
import json

import xml.etree.ElementTree as ET

from fnmatch import fnmatch as match_pattern


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


def rstrip(text):
    return text.rstrip('\r\n')


def load_text(path):
    with open(path) as file:
        return file.read()


def dump_text(text, path):
    with open(path, 'w') as file:
        file.write(text)


def load_lines(path, encoding="utf-8"):
    with open(path, encoding=encoding) as file:
        for line in file:
            yield rstrip(line)


#####
#
#   XML
#
######


def parse_xml(text):
    return ET.fromstring(text)


#########
#
#   GZ, BZ, XZ
#
#####


def load_z_lines(path, open, encoding='utf8'):
    with open(path, mode='rt', encoding=encoding) as file:
        for line in file:
            yield rstrip(line)


def load_gz_lines(path):
    return load_z_lines(path, gzip.open)


def load_bz2_lines(path):
    return load_z_lines(path, bz2.open)


def load_xz_lines(path):
    # Python may be built without lzma support
    # https://github.com/pandas-dev/pandas/issues/27532
    import lzma

    return load_z_lines(path, lzma.open)


#######
#
#   ZIP
#
########


def list_zip(path):
    with ZipFile(path) as zip:
        return zip.namelist()


def load_zip_lines(path, name, encoding='utf8'):
    with ZipFile(path) as zip:
        with zip.open(name) as file:
            for line in file:
                yield rstrip(line.decode(encoding))


def load_zip_texts(path, names, encoding='utf8'):
    with ZipFile(path) as zip:
        for name in names:
            with zip.open(name) as file:
                yield file.read().decode(encoding)


########
#
#   CSV
#
#######


def parse_csv(lines, delimiter=',', max_field=None):
    if max_field:
        csv.field_size_limit(max_field)
    return csv.reader(lines, delimiter=delimiter)


def parse_tsv(lines):
    return parse_csv(lines, delimiter='\t')


def skip_header(rows):
    return next(rows)


def dict_csv(rows):
    header = next(rows)
    for row in rows:
        yield dict(zip(header, row))


#########
#
#    JSONL
#
#######


def parse_jsonl(lines):
    for line in lines:
        yield json.loads(line)
