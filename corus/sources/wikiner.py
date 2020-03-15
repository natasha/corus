
from corus.record import Record
from corus.io import load_bz2_lines


class WikinerToken(Record):
    __attributes__ = ['text', 'pos', 'tag']

    def __init__(self, text, pos, tag):
        self.text = text
        self.pos = pos
        self.tag = tag


class WikinerMarkup(Record):
    __attributes__ = ['tokens']

    def __init__(self, tokens):
        self.tokens = tokens


def parse_wikiner(line):
    if not line:
        # skip empy lines
        return

    # На|PR|O севере|S|O граничит|V|O с|PR|O Латвией|S|I-LOC
    tokens = []
    for part in line.split():
        text, pos, tag = part.split('|', 2)
        token = WikinerToken(text, pos, tag)
        tokens.append(token)

    return WikinerMarkup(tokens)


def load_wikiner(path):
    lines = load_bz2_lines(path)
    for line in lines:
        record = parse_wikiner(line)
        if record:
            yield record
