
import gzip
import bz2

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
