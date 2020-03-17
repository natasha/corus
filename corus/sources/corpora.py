
from corus.record import Record
from corus.io import (
    list_zip,
    load_zip_texts,
    parse_xml
)


class CorporaText(Record):
    __attributes__ = ['id', 'parent_id', 'name', 'tags', 'pars']

    def __init__(self, id, parent_id, name, tags, pars):
        self.id = id
        self.parent_id = parent_id
        self.name = name
        self.tags = tags
        self.pars = pars


class CorporaPar(Record):
    __attributes__ = ['id', 'sents']

    def __init__(self, id, sents):
        self.id = id
        self.sents = sents


class CorporaSent(Record):
    __attributes__ = ['id', 'text', 'tokens']

    def __init__(self, id, text, tokens):
        self.id = id
        self.text = text
        self.tokens = tokens


class CorporaToken(Record):
    __attributes__ = ['id', 'rev_id', 'text', 'forms']

    def __init__(self, id, rev_id, text, forms):
        self.id = id
        self.rev_id = rev_id
        self.text = text
        self.forms = forms


class CorporaForm(Record):
    __attributes__ = ['id', 'text', 'grams']

    def __init__(self, id, text, grams):
        self.id = id
        self.text = text
        self.grams = grams


# <?xml version="1.0" encoding="UTF-8"?>
# <text parent="226" name="18043 Так кто кому должен?" id="374">
#    <tags>
#       <tag>url:http://www.chaskor.ru/news/tak_kto_komu_dolzhen_18043</tag>
#       <tag>Год:2010</tag>
#       <tag>Дата:19/06</tag>
#       <tag>Тема:ЧасКор:Экономика</tag>
#       <tag>Тема:ЧасКор:Экономика/Сырье</tag>
#    </tags>
#    <paragraphs>
#       <paragraph id="5661">
#          <sentence id="17247">
#             <source>Так кто кому должен?</source>
#             <tokens>
#                <token text="Так" id="321074">
#                   <tfr rev_id="1154582" t="Так">
#                      <v>
#                         <l t="так" id="342451">
#                            <g v="CONJ" />
#                         </l>
#                      </v>
#                      <v>
#                         <l t="так" id="342452">
#                            <g v="PRCL" />
#                         </l>
#                      </v>


def parse_grams(xml):
    for item in xml:
        yield item.get('v')


def parse_forms(xml):
    for item in xml:
        lemma = item.find('l')
        id = lemma.get('id')
        text = lemma.get('t')
        grams = list(parse_grams(lemma))
        yield CorporaForm(id, text, grams)


def parse_tokens(xml):
    for token in xml:
        id = token.get('id')
        text = token.get('text')
        forms = token.find('tfr')
        rev_id = forms.get('rev_id')
        forms = list(parse_forms(forms))
        yield CorporaToken(id, rev_id, text, forms)


def parse_sents(xml):
    for sent in xml:
        id = sent.get('id')
        source, tokens = sent
        text = source.text
        tokens = list(parse_tokens(tokens))
        yield CorporaSent(id, text, tokens)


def parse_pars(xml):
    for par in xml:
        id = par.get('id')
        sents = list(parse_sents(par))
        yield CorporaPar(id, sents)


def parse_tags(xml):
    for tag in xml:
        yield tag.text


def parse_text(xml):
    id = xml.get('id')
    parent_id = xml.get('parent')
    name = xml.get('name')
    tags, pars = xml
    tags = list(parse_tags(tags))
    pars = list(parse_pars(pars))
    return CorporaText(id, parent_id, name, tags, pars)


def load_corpora(path):
    names = list_zip(path)
    texts = load_zip_texts(path, names)
    for text in texts:
        xml = parse_xml(text)
        yield parse_text(xml)
