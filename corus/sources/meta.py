
from corus.record import Record

from . import (
    load_factru,
    load_gareev,
    load_lenta,
    load_librusec,
    load_ne5,
    load_wikiner,

    load_taiga_arzamas,
    load_taiga_fontanka,
    load_taiga_interfax,
    load_taiga_kp,
    load_taiga_lenta,
    load_taiga_nplus1,
    load_taiga_magazines,
    load_taiga_subtitles,
    load_taiga_social,
    load_taiga_proza,
    load_taiga_stihi,

    load_buriy_lenta,
    load_buriy_news,
    load_buriy_webhose,

    load_mokoron,
    load_wiki
)


class Meta(Record):
    __attributes__ = ['title', 'url',
                      'description', 'stats', 'instruction',
                      'tags', 'functions']

    def __init__(self, title, url=None,
                 description=None, stats=None, instruction=(),
                 tags=(), functions=()):
        self.title = title
        self.url = url
        self.description = description
        self.stats = stats
        self.instruction = instruction
        self.tags = tags
        self.functions = functions


class Stats(Record):
    __attributes__ = ['bytes', 'count']

    def __init__(self, bytes=None, count=None):
        self.bytes = bytes
        self.count = count


NER = 'ner'
NEWS = 'news'
LIT = 'lit'
SOCIAL = 'social'

METAS = [
    Meta(
        title='Lenta.ru',
        url='https://github.com/yutkin/Lenta.Ru-News-Dataset',
        description='Dump of lenta.ru',
        stats=Stats(
            bytes=1785632079,
            count=739351
        ),
        instruction=[
            'wget https://github.com/yutkin/Lenta.Ru-News-Dataset/releases/download/v1.0/lenta-ru-news.csv.gz'
        ],
        tags=[NEWS],
        functions=[load_lenta]
    ),
    Meta(
        title='Lib.rus.ec',
        url='https://russe.nlpub.org/downloads/',
        description='Dump of lib.rus.ec prepared for RUSSE workshop',
        stats=Stats(
            count=301871,
            bytes=155611193945
        ),
        instruction=[
            'wget http://panchenko.me/data/russe/librusec_fb2.plain.gz'
        ],
        tags=[LIT],
        functions=[load_librusec]
    ),


    ###########
    #
    #    NER
    #
    ############


    Meta(
        title='factRuEval-2016',
        url='https://github.com/dialogue-evaluation/factRuEval-2016/',
        description='Manual PER, LOC, ORG markup prepared for 2016 Dialog competition.',
        stats=Stats(
            count=254,
            bytes=992532
        ),
        instruction=[
            'wget https://github.com/dialogue-evaluation/factRuEval-2016/archive/master.zip',
            'unzip master.zip',
            'rm master.zip'
        ],
        tags=[NER, NEWS],
        functions=[load_factru]
    ),
    Meta(
        title='Gareev',
        url='https://www.researchgate.net/publication/262203599_Introducing_Baselines_for_Russian_Named_Entity_Recognition',
        description='Manual PER, ORG markup.',
        stats=Stats(
            count=97,
            bytes=465938
        ),
        instruction=[
            'Email Rinat Gareev (gareev-rm@yandex.ru) ask for dataset',
            'tar -xvf rus-ner-news-corpus.iob.tar.gz',
            'rm rus-ner-news-corpus.iob.tar.gz'
        ],
        tags=[NER, NEWS],
        functions=[load_gareev]
    ),
    Meta(
        title='Collection5',
        url='http://www.labinform.ru/pub/named_entities/',
        description='News articles with manual PER, LOC, ORG markup.',
        stats=Stats(
            count=1000,
            bytes=3105146
        ),
        instruction=[
            'wget http://www.labinform.ru/pub/named_entities/collection5.zip',
            'unzip collection5.zip',
            'rm collection5.zip'
        ],
        tags=[NER, NEWS],
        functions=[load_ne5]
    ),
    Meta(
        title='WiNER',
        url='https://www.aclweb.org/anthology/I17-1042',
        description='Sentences from Wiki auto annotated with PER, LOC, ORG tags.',
        stats=Stats(
            count=203287,
            bytes=37907651
        ),
        instruction=[
            'wget https://github.com/dice-group/FOX/raw/master/input/Wikiner/aij-wikiner-ru-wp3.bz2'
        ],
        tags=[NER],
        functions=[load_wikiner]
    ),


    ##########
    #
    #    TAIGA
    #
    ###########


    Meta(
        title='Taiga',
        url='https://tatianashavrina.github.io/taiga_site/',
        description='Large collection of russian texts from various sources: news sites, magazines, literacy, social networks.',
        instruction=[
            'wget https://linghub.ru/static/Taiga/retagged_taiga.tar.gz',
            'tar -xzvf retagged_taiga.tar.gz'
        ]
    ),
    Meta(
        title='Taiga/Arzamas',
        description='Dump of arzamas.academy.',
        stats=Stats(
            count=311,
            bytes=4721604
        ),
        tags=[NEWS],
        functions=[load_taiga_arzamas],
    ),
    Meta(
        title='Taiga/Fontanka',
        description='Dump of fontanka.ru.',
        stats=Stats(
            count=342683,
            bytes=824419630
        ),
        tags=[NEWS],
        functions=[load_taiga_fontanka],
    ),
    Meta(
        title='Taiga/Interfax',
        description='Dump of interfax.ru.',
        stats=Stats(
            count=46429,
            bytes=81320006
        ),
        tags=[NEWS],
        functions=[load_taiga_interfax],
    ),
    Meta(
        title='Taiga/KP',
        description='Dump of kp.ru.',
        stats=Stats(
            count=45503,
            bytes=64789612
        ),
        tags=[NEWS],
        functions=[load_taiga_kp],
    ),
    Meta(
        title='Taiga/Lenta',
        description='Dump of lenta.ru.',
        stats=Stats(
            count=36446,
            bytes=99772679
        ),
        tags=[NEWS],
        functions=[load_taiga_lenta],
    ),
    Meta(
        title='Taiga/N+1',
        description='Dump of nplus1.ru.',
        stats=Stats(
            count=7696,
            bytes=26167631
        ),
        tags=[NEWS],
        functions=[load_taiga_nplus1],
    ),
    Meta(
        title='Taiga/Magazines',
        description='Dump of magazines.russ.ru',
        stats=Stats(
            count=39890,
            bytes=2352629006
        ),
        functions=[load_taiga_magazines]
    ),
    Meta(
        title='Taiga/Subtitles',
        stats=Stats(
            count=19011,
            bytes=953237022
        ),
        functions=[load_taiga_subtitles]
    ),
    Meta(
        title='Taiga/Social',
        stats=Stats(
            count=1876442,
            bytes=679670941
        ),
        tags=[SOCIAL],
        functions=[load_taiga_social]
    ),
    Meta(
        title='Taiga/Proza',
        description='Dump of proza.ru',
        stats=Stats(
            count=1732434,
            bytes=41067043857
        ),
        tags=[LIT],
        functions=[load_taiga_proza]
    ),
    Meta(
        title='Taiga/Stihi',
        description='Dump of stihi.ru',
        stats=Stats(
            count=9157686,
            bytes=13745805334
        ),
        functions=[load_taiga_stihi]
    ),


    #############
    #
    #   BURIY
    #
    ##########


    Meta(
        title='Buriy (russian-nlp-datasets)',
        url='https://github.com/buriy/russian-nlp-datasets/releases',
        description='Several russian news datasets from webhose.io, lenta.ru and other news sites.',
    ),
    Meta(
        title='Buriy/Lenta',
        description='Dump of lenta.ru.',
        instruction=[
            'wget https://github.com/buriy/russian-nlp-datasets/releases/download/r4/lenta.tar.bz2',
        ],
        stats=Stats(
            count=699777,
            bytes=1683268809
        ),
        tags=[NEWS],
        functions=[load_buriy_lenta],
    ),
    Meta(
        title='Buriy/News',
        description='Dump of top 40 news + 20 fashion news sites.',
        instruction=[
            'wget https://github.com/buriy/russian-nlp-datasets/releases/download/r4/news-articles-2014.tar.bz2',
            'wget https://github.com/buriy/russian-nlp-datasets/releases/download/r4/news-articles-2015-part1.tar.bz2',
            'wget https://github.com/buriy/russian-nlp-datasets/releases/download/r4/news-articles-2015-part2.tar.bz2'
        ],
        stats=Stats(
            count=2154801,
            bytes=7340672169
        ),
        tags=[NEWS],
        functions=[load_buriy_news],
    ),
    Meta(
        title='Buriy/Webhose',
        description='Dump from webhose.io, 300 sources for one month.',
        instruction=[
            'wget https://github.com/buriy/russian-nlp-datasets/releases/download/r4/stress.tar.gz'
        ],
        stats=Stats(
            count=285965,
            bytes=901066314
        ),
        tags=[NEWS],
        functions=[load_buriy_webhose],
    ),


    #########
    #
    #    MOKORON
    #
    #########


    Meta(
        title='Mokoron Russian Twitter Corpus',
        url='http://study.mokoron.com/',
        description='Russian tweets.',
        instruction=[
            'Manually download https://www.dropbox.com/s/9egqjszeicki4ho/db.sql'
        ],
        stats=Stats(
            count=17633417,
            bytes=1998559570
        ),
        tags=[SOCIAL],
        functions=[load_mokoron],
    ),


    ###########
    #
    #   WIKI
    #
    #########


    Meta(
        title='Wikipedia',
        url='https://dumps.wikimedia.org/',
        description='Russian Wiki dump.',
        instruction=[
            'wget https://dumps.wikimedia.org/ruwiki/latest/ruwiki-latest-pages-articles.xml.bz2'
        ],
        stats=Stats(
            count=1541401,
            bytes=13895798340
        ),
        functions=[load_wiki],
    ),
]
