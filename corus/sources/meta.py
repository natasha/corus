
from ..record import Record

from . import (
    load_factru,
    load_gareev,
    load_lenta,
    load_librusec,
    load_ne5,
    load_wikiner
)


class Meta(Record):
    __attributes__ = ['title', 'url', 'description', 'instruction', 'tags', 'functions']

    def __init__(self, title, url,
                 description=None, instruction=(),
                 tags=(), functions=()):
        self.title = title
        self.url = url
        self.description = description
        self.instruction = instruction
        self.tags = tags
        self.functions = functions


NER = 'ner'
NEWS = 'news'

METAS = [
    Meta(
        title='factRuEval-2016',
        url='https://github.com/dialogue-evaluation/factRuEval-2016/',
        description='254 news articles with manual PER, LOC, ORG markup.',
        instruction=[
            'wget https://github.com/dialogue-evaluation/factRuEval-2016/archive/master.zip',
            'unzip master.zip',
            'rm master.zip'
        ],
        tags=[NER],
        functions=[load_factru]
    ),
    Meta(
        title='Gareev',
        url='https://www.researchgate.net/publication/262203599_Introducing_Baselines_for_Russian_Named_Entity_Recognition',
        description='97 news articles with manual PER, ORG markup.',
        instruction=[
            'Email Rinat Gareev (gareev-rm@yandex.ru) ask for dataset',
            'tar -xvf rus-ner-news-corpus.iob.tar.gz',
            'rm rus-ner-news-corpus.iob.tar.gz'
        ],
        tags=[NER],
        functions=[load_gareev]
    ),
    Meta(
        title='Lenta.ru',
        url='https://github.com/yutkin/Lenta.Ru-News-Dataset',
        description='Dump of lenta.ru, ~790 000 articles, ~1.9Gb of text.',
        instruction=[
            'wget https://github.com/yutkin/Lenta.Ru-News-Dataset/releases/download/v1.0/lenta-ru-news.csv.gz'
        ],
        tags=[NEWS],
        functions=[load_lenta]
    ),
    Meta(
        title='Lib.rus.ec',
        url='https://russe.nlpub.org/downloads/',
        description='Dump of lib.rus.ec prepared for RUSSE workshop, ~150Gb of text.',
        instruction=[
            'wget http://panchenko.me/data/russe/librusec_fb2.plain.gz'
        ],
        functions=[load_librusec]
    ),
    Meta(
        title='Collection5',
        url='http://www.labinform.ru/pub/named_entities/',
        description='1000 news articles with manual PER, LOC, ORG markup.',
        instruction=[
            'wget http://www.labinform.ru/pub/named_entities/collection5.zip',
            'unzip collection5.zip',
            'rm collection5.zip'
        ],
        tags=[NER],
        functions=[load_ne5]
    ),
    Meta(
        title='WiNER',
        url='https://www.aclweb.org/anthology/I17-1042',
        description='~200 000 sentences from Wiki auto annotated with PER, LOC, ORG tags.',
        instruction=[
            'wget https://github.com/dice-group/FOX/raw/master/input/Wikiner/aij-wikiner-ru-wp3.bz2'
        ],
        tags=[NER],
        functions=[load_wikiner]
    ),
    Meta(
        title='Taiga',
        url='https://tatianashavrina.github.io/taiga_site/',
        instruction=[
            'wget https://linghub.ru/static/Taiga/retagged_taiga.tar.gz',
            'tar -xzvf retagged_taiga.tar.gz'
        ]
    )
]
