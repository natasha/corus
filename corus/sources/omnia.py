
import re

from corus.record import Record
from corus.io import load_xz_lines


class OmniaDoc(Record):
    __attributes__ = ['id', 'attrs', 'pars']

    def __init__(self, id, attrs, pars):
        self.id = id
        self.attrs = attrs
        self.pars = pars


class OmniaPar(Record):
    __attributes__ = ['sents']

    def __init__(self, sents):
        self.sents = sents


class OmniaSent(Record):
    __attributes__ = ['tokens']

    def __init__(self, tokens):
        self.tokens = tokens


class OmniaToken(Record):
    __attributes__ = ['text', 'lemma', 'atag', 'tag', 'ztag', 'g']

    def __init__(self, text, lemma, atag, tag, ztag, g):
        self.text = text
        self.lemma = lemma
        self.atag = atag
        self.tag = tag
        self.ztag = ztag
        self.g = g


DID = 'did'
G_TAG = '<g/>'
S_END = '</s>'
P_END = '</p>'
DOC_END = '</doc>'


def take_until(stream, value):
    for item in stream:
        if item == value:
            break
        yield item


def group_bounds(stream, end):
    for _ in stream:
        yield take_until(stream, end)


def group_doc_bounds(stream):
    for header in stream:
        group = take_until(stream, DOC_END)
        yield header, group


def group_pairs(stream):
    previous = None
    for item in stream:
        if previous:
            yield previous, item
        previous = item
    if previous:
        yield previous, None


def parse_tokens(lines):
    pairs = group_pairs(lines)
    for line, next in pairs:
        if line == G_TAG:
            continue

        parts = line.split('\t')
        if len(parts) != 5:
            # наблюдать       наблюдать       Vb      Vmn----a-e      1
            # интерес интерес Nn      Ncmsan  1
            # Э       Э       Zz      -       1
            # <g/>
            # <дуарда>
            # Г       Г       Zz      -       1
            # <g/>
            # <еоргиевича>
            # к       к       Pp      Sp-d    1
            # попыткам        попытка Nn      Ncfpdn  1

            # weird tag lines
            # <нрзб> <НРЗБ>
            # <дуарда>
            # <еоргиевича>

            # just skip them
            continue

        # Refs on atag and tag:
        # http://unesco.uniba.sk/aranea_about/aut.html
        # http://nl.ijs.si/ME/V4/msd/html/msd-ru.html
        text, lemma, atag, tag, ztag = parts
        g = next == G_TAG

        yield OmniaToken(text, lemma, atag, tag, ztag, g)


def parse_sents(lines):
    groups = group_bounds(lines, S_END)
    for group in groups:
        tokens = list(parse_tokens(group))
        yield OmniaSent(tokens)


def parse_pars(lines):
    groups = group_bounds(lines, P_END)
    for group in groups:
        sents = list(parse_sents(group))
        yield OmniaPar(sents)


def parse_tag_attrs(tag):
    matches = re.finditer(r'([^= ]+)="([^"]+)"', tag)
    for match in matches:
        yield match.groups()


def parse_doc_header(header):
    attrs = dict(parse_tag_attrs(header))
    id = attrs.pop(DID)
    return id, attrs


def parse_docs(lines):
    groups = group_doc_bounds(lines)
    for header, group in groups:
        id, attrs = parse_doc_header(header)
        pars = list(parse_pars(group))
        yield OmniaDoc(id, attrs, pars)


def load_omnia(path):
    lines = load_xz_lines(path)
    yield from parse_docs(lines)
