
from collections import namedtuple

import zlib
from contextlib import contextmanager
from os import SEEK_END
from struct import (
    calcsize,
    unpack
)

from corus.record import Record


#############
#
#   SPECS
#
##########


#    File:    APPNOTE.TXT - .ZIP File Format Specification
#       https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT

#    4.3.16  End of central directory record:
#       end of central dir signature    4 bytes  (0x06054b50)
#       number of this disk             2 bytes
#       number of the disk with the
#       start of the central directory  2 bytes
#       total number of entries in the
#       central directory on this disk  2 bytes
#       total number of entries in
#       the central directory           2 bytes
#       size of the central directory   4 bytes
#       offset of start of central
#       directory with respect to
#       the starting disk number        4 bytes
#       .ZIP file comment length        2 bytes
#       .ZIP file comment       (variable size)


ECD_FORMAT = '<4s4H2LH'
ECD_SIGNATURE = b'PK\x05\x06'


Ecd = namedtuple(
    'Ecd',
    ['signature', 'disks', 'disk', 'records', 'total', 'size', 'offset', 'comment']
)


def extract_ecd(file):
    size = calcsize(ECD_FORMAT)
    file.seek(-size, SEEK_END)
    buffer = file.read(size)
    data = unpack(ECD_FORMAT, buffer)
    ecd = Ecd._make(data)
    assert_ecd(ecd)
    return ecd


def assert_ecd(record):
    assert record.signature == ECD_SIGNATURE
    assert record.disks == 0
    assert record.disk == 0
    assert record.records == record.total
    assert record.comment == 0


#    4.3.15 Zip64 end of central directory locator
#       zip64 end of central dir locator
#       signature                       4 bytes  (0x07064b50)
#       number of the disk with the
#       start of the zip64 end of
#       central directory               4 bytes
#       relative offset of the zip64
#       end of central directory record 8 bytes
#       total number of disks           4 bytes


ECD64_LOCATOR_FORMAT = '<4sLQL'
ECD64_LOCATOR_SIGNATURE = b'PK\x06\x07'


Ecd64Locator = namedtuple(
    'Ecd64Locator',
    ['signature', 'disk', 'offset', 'disks']
)


def extract_ecd64_locator(file):
    offset = calcsize(ECD_FORMAT)
    size = calcsize(ECD64_LOCATOR_FORMAT)
    file.seek(-offset - size, SEEK_END)
    buffer = file.read(size)
    data = unpack(ECD64_LOCATOR_FORMAT, buffer)
    locator = Ecd64Locator._make(data)
    assert_ecd64_locator(locator)
    return locator


def assert_ecd64_locator(record):
    assert record.signature == ECD64_LOCATOR_SIGNATURE
    assert record.disk == 0
    assert record.disks == 1


#    4.3.14  Zip64 end of central directory record
#         zip64 end of central dir
#         signature                       4 bytes  (0x06064b50)
#         size of zip64 end of central
#         directory record                8 bytes
#         version made by                 2 bytes
#         version needed to extract       2 bytes
#         number of this disk             4 bytes
#         number of the disk with the
#         start of the central directory  4 bytes
#         total number of entries in the
#         central directory on this disk  8 bytes
#         total number of entries in the
#         central directory               8 bytes
#         size of the central directory   8 bytes
#         offset of start of central
#         directory with respect to
#         the starting disk number        8 bytes
#         zip64 extensible data sector    (variable size)


ECD64_FORMAT = '<4sQ2H2L4Q'
ECD64_SIGNATURE = b'PK\x06\x06'


Ecd64 = namedtuple(
    'Ecd64',
    ['signature', 'rest', 'made_by', 'extract_by',
     'disk', 'disks', 'records', 'total', 'size', 'offset']
)


def extract_ecd64(file):
    offset = calcsize(ECD_FORMAT) + calcsize(ECD64_LOCATOR_FORMAT)
    size = calcsize(ECD64_FORMAT)
    file.seek(-offset - size, SEEK_END)
    buffer = file.read(size)
    data = unpack(ECD64_FORMAT, buffer)
    ecd = Ecd64._make(data)
    assert_ecd64(ecd)
    return ecd


def assert_ecd64(record):
    assert record.signature == ECD64_SIGNATURE
    assert record.rest == 44  # 4.3.14.1
    assert record.disk == 0
    assert record.disks == 0
    assert record.records == record.total


#    4.3.12  Central directory structure:
#       File header:
#         central file header signature   4 bytes  (0x02014b50)
#         version made by                 2 bytes
#         version needed to extract       2 bytes
#         general purpose bit flag        2 bytes
#         compression method              2 bytes
#         last mod file time              2 bytes
#         last mod file date              2 bytes
#         crc-32                          4 bytes
#         compressed size                 4 bytes
#         uncompressed size               4 bytes
#         file name length                2 bytes
#         extra field length              2 bytes
#         file comment length             2 bytes
#         disk number start               2 bytes
#         internal file attributes        2 bytes
#         external file attributes        4 bytes
#         relative offset of local header 4 bytes

#         file name (variable size)
#         extra field (variable size)
#         file comment (variable size)


CDR_FORMAT = '<4s6H3L5H2L'
CDR_SIGNATURE = b'PK\x01\x02'

NO_COMPRESSION = 0
DEFLATED = 8


Cdr = namedtuple(
    'Cdr',
    ['signature', 'made_by', 'extract_by', 'flags', 'compression',
     'time', 'date', 'crc', 'compressed', 'uncompressed',
     'name', 'extra', 'comment',
     'disk', 'internal', 'external', 'offset']
)


# 4.5 Extensible data fields
# --------------------------

#    4.5.1 In order to allow different programs and different types
#    of information to be stored in the 'extra' field in .ZIP
#    files, the following structure MUST be used for all
#    programs storing data in this field:

#        header1+data1 + header2+data2 . . .

#    Each header MUST consist of:

#        Header ID - 2 bytes
#        Data Size - 2 bytes


#   4.5.3 -Zip64 Extended Information Extra Field (0x0001):
#       The following is the layout of the zip64 extended
#       information "extra" block. If one of the size or
#       offset fields in the Local or Central directory
#       record is too small to hold the required data,
#       a Zip64 extended information record is created.
#       The order of the fields in the zip64 extended
#       information record is fixed, but the fields MUST
#       only appear if the corresponding Local or Central
#       directory record field is set to 0xFFFF or 0xFFFFFFFF.

#       Note: all fields stored in Intel low-byte/high-byte order.

#         Value      Size       Description
#         -----      ----       -----------
# (ZIP64) 0x0001     2 bytes    Tag for this "extra" block type
#         Size       2 bytes    Size of this "extra" block
#         Original
#         Size       8 bytes    Original uncompressed file size
#         Compressed
#         Size       8 bytes    Size of compressed data
#         Relative Header
#         Offset     8 bytes    Offset of local header record
#         Disk Start
#         Number     4 bytes    Number of the disk on which
#                               this file starts


def has_extra(record):
    return record.offset == 0xffffffff


def assert_extra(record):
    # assert extra has just offset
    assert record.uncompressed not in (0xffffffffffffffff, 0xffffffff)
    assert record.compressed != 0xffffffff


SHORT2_FORMAT = '<HH'
SHORT2 = calcsize(SHORT2_FORMAT)
LONG_FORMAT = '<Q'
LONG = calcsize(LONG_FORMAT)
ZIP64 = 1


def decode_extra(data):
    while len(data) >= SHORT2:
        buffer = data[:SHORT2]
        id, size = unpack(SHORT2_FORMAT, buffer)
        if id == ZIP64:
            assert size == LONG
            buffer = data[SHORT2:SHORT2 + LONG]
            offset, = unpack(LONG_FORMAT, buffer)
            return offset
        data = data[SHORT2 + size:]
    raise


def decode_name(name):
    # since assert flags == 0
    return name.decode('cp437')


def extract_cdrs(file, ecd):
    file.seek(ecd.offset)
    size = calcsize(CDR_FORMAT)
    for _ in range(ecd.records):
        buffer = file.read(size)
        data = unpack(CDR_FORMAT, buffer)
        cdr = Cdr._make(data)
        assert_cdr(cdr)
        name = file.read(cdr.name)
        cdr = cdr._replace(name=decode_name(name))
        extra = file.read(cdr.extra)
        if has_extra(cdr):
            assert_extra(cdr)
            offset = decode_extra(extra)
            cdr = cdr._replace(offset=offset)
        file.read(cdr.comment)  # skip comment
        yield cdr


def assert_cdr(record):
    assert record.signature == CDR_SIGNATURE
    assert record.flags == 0
    assert record.compression in (NO_COMPRESSION, DEFLATED)
    assert record.disk == 0


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


LFH_FORMAT = '<4s5HL2L2H'
LFH_SIGNATURE = b'PK\x03\x04'


Lfh = namedtuple(
    'Lfh',
    ['signature', 'extract_by', 'flags', 'compression',
     'time', 'date', 'crc', 'compressed', 'uncompressed',
     'name', 'extra']
)


def extract_lfh(file):
    size = calcsize(LFH_FORMAT)
    buffer = file.read(size)
    data = unpack(LFH_FORMAT, buffer)
    lfh = Lfh._make(data)
    assert_lfh(lfh)
    name = file.read(lfh.name)
    lfh = lfh._replace(name=decode_name(name))
    file.read(lfh.extra)  # skip extra
    return lfh


def assert_lfh(record):
    assert record.signature == LFH_SIGNATURE
    assert record.flags == 0
    assert record.compression in (NO_COMPRESSION, DEFLATED)


def extract_data(file, header):
    data = file.read(header.compressed)
    if header.compression == DEFLATED:
        data = zlib.decompress(data, -15)
    return data


#########
#
#   API
#
########


class ZipRecord(Record):
    __attributes__ = ['name', 'offset', 'compressed', 'uncompressed']

    def __init__(self, name, offset, compressed, uncompressed):
        self.name = name
        self.offset = offset
        self.compressed = compressed
        self.uncompressed = uncompressed

    @classmethod
    def from_cdr(cls, cdr):
        return ZipRecord(
            cdr.name,
            cdr.offset,
            cdr.compressed,
            cdr.uncompressed
        )


class ZipDir(Record):
    __attributes__ = ['size', 'records']

    def __init__(self, size, records):
        self.size = size
        self.records = records

    def __iter__(self):
        return self.records


def open_zip(path):
    return open(path, 'rb')


@contextmanager
def seeked(file, offset):
    previous = file.tell()
    file.seek(offset)
    yield file
    file.seek(previous)


def list_zip(zip):
    ecd = extract_ecd64(zip)
    cdrs = extract_cdrs(zip, ecd)
    return ZipDir(
        size=ecd.records,
        records=(ZipRecord.from_cdr(_) for _ in cdrs)
    )


def read_zip(zip, record, encoding='utf8'):
    with seeked(zip, record.offset):
        header = extract_lfh(zip)
        data = extract_data(zip, header)
        return data.decode(encoding)
