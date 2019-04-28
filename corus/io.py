
import gzip
import bz2
import tarfile

import csv
import json

import xml.etree.ElementTree as ET

from fnmatch import fnmatch as match_pattern

from .record import Record
from .zip import (
    open_zip,
    read_zip_header,
    read_zip_data
)


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


def load_gz_lines(path, encoding='utf8', gzip=gzip):
    with gzip.open(path, mode='rt', encoding=encoding) as file:
        for line in file:
            yield line.rstrip()


########
#
#    BZ
#
########


def load_bz2_lines(path, encoding='utf8'):
    return load_gz_lines(path, encoding=encoding, gzip=bz2)


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


#########
#
#    JSONL
#
#######


def parse_jsonl(lines):
    for line in lines:
        yield json.loads(line)


#######
#
#   TAR
#
######


class TarRecord(Record):
    __attributes__ = ['name', 'offset', 'file']

    def __init__(self, name, offset, file):
        self.name = name
        self.offset = offset
        self.file = file


def load_tar(path, offset=0):
    with tarfile.open(path) as tar:
        tar.fileobj.seek(offset)
        while True:
            member = tarfile.TarInfo.fromtarfile(tar)
            if not member.isfile():
                continue

            file = tar.extractfile(member)
            yield TarRecord(
                name=member.name,
                offset=member.offset,
                file=file
            )

            tar.members = []
            tar.fileobj.seek(tar.offset)


#######
#
#   ZIP
#
######


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
