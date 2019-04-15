
import gzip
import bz2
import csv
import json
import xml.etree.ElementTree as ET


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


def parse_csv(lines, header=True):
    if header:
        next(lines)
    return csv.reader(lines)


def parse_jsonl(lines):
    for line in lines:
        yield json.loads(line)
