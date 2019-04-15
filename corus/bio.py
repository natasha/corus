
from .record import Record


B = 'B'
I = 'I'
O = 'O'


class Span(Record):
    __attributes__ = ['start', 'stop', 'type']

    def __init__(self, start, stop, type):
        self.start = start
        self.stop = stop
        self.type = type


def parse_bio(tag):
    if '-' in tag:
        part, type = tag.split('-', 1)
    else:
        part = tag
        type = None
    if part not in (B, I, O):
        raise ValueError(tag)
    return part, type


def bio_spans(tokens, tags):
    previous = None
    start = None
    stop = None
    for token, tag in zip(tokens, tags):
        part, type = parse_bio(tag)
        if part == O:
            if previous:
                yield Span(start, stop, previous)
                previous = None
        elif part == B:
            if previous:
                yield Span(start, stop, previous)
            previous = type
            start = token.start
            stop = token.stop
        elif part == I:
            stop = token.stop
    if previous:
        yield Span(start, stop, previous)


def io_spans(tokens, tags):
    previous = None
    start = None
    stop = None
    for token, tag in zip(tokens, tags):
        part, type = parse_bio(tag)
        # wikiner splits on I-PER B-PER for example
        if previous != type or part == B:
            if not previous and type:
                # O I
                start = token.start
            elif previous and type:
                # I-A I-B
                yield Span(start, stop, previous)
                start = token.start
            elif previous and not type:
                # I O
                yield Span(start, stop, previous)
                previous = None
        previous = type
        stop = token.stop
    if previous:
        yield Span(start, stop, previous)
