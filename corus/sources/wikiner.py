# coding: utf8

from corus.record import Record
from corus.io import load_bz2_lines
from corus.bio import io_spans
from corus.token import find_tokens


class WikinerMarkup(Record):
    __attributes__ = ['text', 'spans']

    def __init__(self, text, spans):
        self.text = text
        self.spans = spans


def parse_wikiner(line):
    if not line:
        # skip empy lines
        return

    # На|PR|O севере|S|O граничит|V|O с|PR|O Латвией|S|I-LOC
    chunks = []
    tags = []
    for part in line.split():
        chunk, pos, tag = part.split('|', 2)
        chunks.append(chunk)
        tags.append(tag)
    text = ' '.join(chunks)
    tokens = list(find_tokens(chunks, text))
    spans = list(io_spans(tokens, tags))
    return WikinerMarkup(text, spans)


def load_wikiner(path):
    lines = load_bz2_lines(path)
    for line in lines:
        record = parse_wikiner(line)
        if record:
            yield record
