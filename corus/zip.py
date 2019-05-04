from __future__ import absolute_import  # for from io import BytesIO

from collections import namedtuple

import zlib
from io import BytesIO
from struct import (
    calcsize,
    unpack
)


def open_zip(path):
    return open(path, 'rb')


#    File:    APPNOTE.TXT - .ZIP File Format Specification
#       https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT

#    4.3.7  Local file header:
#       local file header signature     4 bytes  (0x04034b50)
#       version needed to extract       2 bytes
#       general purpose bit flag        2 bytes
#       compression method              2 bytes
#       last mod file time              2 bytes
#       last mod file date              2 bytes
#       crc-32                          4 bytes
#       compressed size                 4 bytes
#       uncompressed size               4 bytes
#       file name length                2 bytes
#       extra field length              2 bytes

#       file name (variable size)
#       extra field (variable size)


HEADER_FORMAT = '<4s5HL2L2H'
HEADER_SIGNATURE = b'PK\x03\x04'

NO_COMPRESSION = 0
DEFLATED = 8


ZipHeader = namedtuple(
    'ZipHeader',
    ['signature', 'extract_by', 'flags', 'compression',
     'time', 'date', 'crc', 'compressed', 'uncompressed',
     'name', 'extra']
)


def decode_name(name):
    # since assert flags == 0
    return name.decode('cp437')


def read_zip_header(file):
    size = calcsize(HEADER_FORMAT)
    buffer = file.read(size)
    if len(buffer) < size:
        return

    data = unpack(HEADER_FORMAT, buffer)
    header = ZipHeader._make(data)
    if not is_zip_header(header):
        return

    assert_zip_header(header)
    name = file.read(header.name)
    header = header._replace(name=decode_name(name))
    file.read(header.extra)  # skip extra
    return header


def is_zip_header(record):
    return record.signature == HEADER_SIGNATURE


def assert_zip_header(record):
    assert record.flags == 0, record.flga
    assert record.compression in (NO_COMPRESSION, DEFLATED), record.compression


def read_zip_data(file, header):
    data = file.read(header.compressed)
    if header.compression == DEFLATED:
        data = zlib.decompress(data, -15)
    # TODO Maybe do buffered reading to save memory
    return BytesIO(data)
