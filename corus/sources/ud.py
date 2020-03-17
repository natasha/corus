
from corus.record import Record
from corus.io import load_lines


class UDSent(Record):
    __attributes__ = ['id', 'text', 'attrs', 'tokens']

    def __init__(self, id, text, attrs, tokens):
        self.id = id
        self.text = text
        self.attrs = attrs
        self.tokens = tokens


class UDToken(Record):
    __attributes__ = ['id', 'text', 'lemma', 'pos', 'feats', 'head_id', 'rel']

    def __init__(self, id, text, lemma, pos, feats, head_id, rel):
        self.id = id
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.feats = feats
        self.head_id = head_id
        self.rel = rel


def group_sents(lines):
    buffer = []
    for line in lines:
        if not line:
            yield buffer
            buffer = []
        else:
            buffer.append(line)
    if buffer:
        yield buffer


def parse_feats(tags):
    if not tags:
        return

    for pair in tags.split('|'):
        key, value = pair.split('=', 1)
        yield key, value


def _none(value):
    if value == '_':
        return
    return value


def parse_row(line):
    return [_none(_) for _ in line.split('\t')]


def parse_attr(line):
    # newdoc
    # title = instagram-2019
    # newpar
    # sent_id = instagram-1
    # speaker = screened-18

    line = line.lstrip('# ')
    if ' = ' in line:
        return line.split(' = ', 1)
    else:
        return line, None


def parse_token(line):
    id, text, lemma, pos, _, feats, head_id, rel, _, _ = parse_row(line)
    feats = dict(parse_feats(feats))
    return UDToken(id, text, lemma, pos, feats, head_id, rel)


def parse_ud(lines):
    # newdoc id = n01001
    # sent_id = n01001011
    # text = «Если передача цифровых технологий сегодня
    # 1       «       «       PUNCT   ``      _       19      punct   _       SpaceA
    # 2       Если    если    SCONJ   IN      _       9       mark    _       _
    # 3       передача        передача        NOUN    NN      Animacy=Inan|Case=N

    for group in group_sents(lines):
        attrs = {}
        tokens = []
        for line in group:
            if line.startswith('#'):
                key, value = parse_attr(line)
                attrs[key] = value
            else:
                token = parse_token(line)
                tokens.append(token)

        id = attrs.pop('sent_id')
        text = attrs.pop('text', None)
        yield UDSent(id, text, attrs, tokens)


def load_ud(path):
    lines = load_lines(path)
    return parse_ud(lines)


def load_ud_gsd(path):
    return load_ud(path)


def load_ud_taiga(path):
    return load_ud(path)


def load_ud_pud(path):
    return load_ud(path)


def load_ud_syntag(path):
    return load_ud(path)


__all__ = [
    'load_ud_gsd',
    'load_ud_taiga',
    'load_ud_pud',
    'load_ud_syntag',
]
