
from corus.record import Record
from corus.io import load_lines

from .ud import group_sents, parse_row, parse_feats


class MorphoSent(Record):
    __attributes__ = ['tokens', 'attrs']

    def __init__(self, tokens, attrs=()):
        self.tokens = tokens
        self.attrs = attrs


class MorphoToken(Record):
    __attributes__ = ['text', 'lemma', 'pos', 'feats', 'feats2']

    def __init__(self, text, lemma, pos, feats, feats2=None):
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.feats = feats
        self.feats2 = feats2


def parse_morphoru(lines, parse_sent):
    for group in group_sents(lines):
        tokens = list(parse_sent(group))
        yield MorphoSent(tokens)


def parse_morphoru_gicrya_sent(lines):
    for line in lines:
        _, text, lemma, pos, feats = parse_row(line)
        feats = dict(parse_feats(feats))
        yield MorphoToken(text, lemma, pos, feats)


def parse_morphoru_corpora_sent(lines):
    for line in lines:
        parts = parse_row(line)
        _, text, lemma, pos, _, feats = parts[:6]
        feats = dict(parse_feats(feats))
        yield MorphoToken(text, lemma, pos, feats)


def parse_morphoru_rnc(lines):
    # ==> blogs.xhtml <==
    # ==newfile==
    #         Кстати  кстати  H       _       _
    #         о       о       ADP     _       _

    for group in group_sents(lines):
        attrs, tokens = [], []
        for line in group:
            if line.startswith('=='):
                attrs.append(line)
            else:
                _, text, lemma, pos, feats, feats2 = parse_row(line)
                feats = dict(parse_feats(feats))
                feats2 = dict(parse_feats(feats2))
                token = MorphoToken(text, lemma, pos, feats, feats2)
                tokens.append(token)
        yield MorphoSent(tokens, attrs)


def load_morphoru_gicrya(path):
    lines = load_lines(path)
    return parse_morphoru(lines, parse_morphoru_gicrya_sent)


def load_morphoru_rnc(path):
    lines = load_lines(path)
    return parse_morphoru_rnc(lines)


def load_morphoru_corpora(path):
    lines = load_lines(path)
    return parse_morphoru(lines, parse_morphoru_corpora_sent)


__all__ = [
    'load_morphoru_gicrya',
    'load_morphoru_rnc',
    'load_morphoru_corpora'
]
