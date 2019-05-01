
import re

from corus.record import Record
from corus.io import load_gz_lines


class LibrusecRecord(Record):
    __attributes__ = ['id', 'text']

    def __init__(self, id, text):
        self.id = id
        self.text = text


def flush(id, buffer):
    return LibrusecRecord(id, '\n'.join(buffer))


def parse_librusec(lines):
    id = None
    buffer = []
    for line in lines:
        match = re.match(r'^(\d+)\.fb2', line)
        if match:
            if id:
                yield flush(id, buffer)
                buffer = []
            id = match.group(1)
            line = line[match.end() + 1:]  # extra space
        buffer.append(line)
    yield flush(id, buffer)


def load_librusec(path):
    lines = load_gz_lines(path)
    return parse_librusec(lines)
