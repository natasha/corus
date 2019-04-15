
from ..meta import Meta
from ..record import Record
from ..io import load_bz2_lines
from ..bio import io_spans
from ..token import find_tokens


META = Meta(
    label='wikiner',
    title='WiNER',
    source='https://www.aclweb.org/anthology/I17-1042',
    description='~200 000 sentences from Wiki automaticaly annotated with PER, LOC, ORG tags.',
    instruction=[
        'wget https://github.com/dice-group/FOX/raw/master/input/Wikiner/aij-wikiner-ru-wp3.bz2'
    ]
)


class WikinerMarkup(Record):
    __attributes__ = ['text', 'spans']

    def __init__(self, text, spans):
        self.text = text
        self.spans = spans


def parse(line):
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


def load(path):
    lines = load_bz2_lines(path)
    for line in lines:
        record = parse(line)
        if record:
            yield record
