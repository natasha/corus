
from .record import Record


class Token(Record):
    __attributes__ = ['start', 'stop', 'text']

    def __init__(self, start, stop, text):
        self.start = start
        self.stop = stop
        self.text = text


def find_tokens(chunks, text):
    offset = 0
    for chunk in chunks:
        start = text.find(chunk, offset)
        stop = start + len(chunk)
        yield Token(start, stop, chunk)
        offset = stop
