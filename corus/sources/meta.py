
from corus.record import Record

from . import (
    load_factru,
    load_gareev,
    load_lenta,
    load_librusec,
    load_ne5,
    load_wikiner,
    load_bsnlp,
    load_persons,

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
    load_wiki,

    load_ods_interfax,
    load_ods_gazeta,

    load_ria_raw,
    load_ria,
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


class Group(Record):
    __attributes__ = ['title', 'url', 'description', 'instruction', 'metas']

    def __init__(self, title, url=None, description=None, instruction=(), metas=()):
        self.title = title
        self.url = url
        self.description = description
        self.instruction = instruction
        self.metas = metas


def is_group(item):
    return isinstance(item, Group)


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
    Meta(
        title='Rossiya Segodnya',
        url='https://github.com/RossiyaSegodnya/ria_news_dataset',
        description=None,
        stats=Stats(
            count=1003869,
            bytes=3974121040
        ),
        instruction=[
            'wget https://github.com/RossiyaSegodnya/ria_news_dataset/raw/master/ria.json.gz'
        ],
        tags=[NEWS],
        functions=[load_ria_raw, load_ria]
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
    Meta(
        title='BSNLP-2019',
        url='http://bsnlp.cs.helsinki.fi/shared_task.html',
        description='Markup prepared for 2019 BSNLP Shared Task',
        stats=Stats(
            count=464,
            bytes=1211300
        ),
        instruction=[
            'wget http://bsnlp.cs.helsinki.fi/TRAININGDATA_BSNLP_2019_shared_task.zip',
            'wget http://bsnlp.cs.helsinki.fi/TESTDATA_BSNLP_2019_shared_task.zip',
            'unzip TRAININGDATA_BSNLP_2019_shared_task.zip',
            'unzip TESTDATA_BSNLP_2019_shared_task.zip -d test_pl_cs_ru_bg',
            'rm TRAININGDATA_BSNLP_2019_shared_task.zip TESTDATA_BSNLP_2019_shared_task.zip'
        ],
        tags=[NER],
        functions=[load_bsnlp]
    ),
    Meta(
        title='Persons-1000',
        url='http://ai-center.botik.ru/Airec/index.php/ru/collections/28-persons-1000',
        description='PER ',
        stats=Stats(
            count=1000,
            bytes=3105146
        ),
        instruction=[
            'wget http://ai-center.botik.ru/Airec/ai-resources/Persons-1000.zip'
        ],
        tags=[NER, NEWS],
        functions=[load_persons]
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


    ##########
    #
    #    TAIGA
    #
    ###########


    Group(
        title='Taiga',
        url='https://tatianashavrina.github.io/taiga_site/',
        description='Large collection of Russian texts from various sources: news sites, magazines, literacy, social networks.',
        instruction=[
            'wget https://linghub.ru/static/Taiga/retagged_taiga.tar.gz',
            'tar -xzvf retagged_taiga.tar.gz'
        ],
        metas=[
            Meta(
                title='Arzamas',
                description='Dump of arzamas.academy.',
                stats=Stats(
                    count=311,
                    bytes=4721604
                ),
                tags=[NEWS],
                functions=[load_taiga_arzamas],
            ),
            Meta(
                title='Fontanka',
                description='Dump of fontanka.ru.',
                stats=Stats(
                    count=342683,
                    bytes=824419630
                ),
                tags=[NEWS],
                functions=[load_taiga_fontanka],
            ),
            Meta(
                title='Interfax',
                description='Dump of interfax.ru.',
                stats=Stats(
                    count=46429,
                    bytes=81320006
                ),
                tags=[NEWS],
                functions=[load_taiga_interfax],
            ),
            Meta(
                title='KP',
                description='Dump of kp.ru.',
                stats=Stats(
                    count=45503,
                    bytes=64789612
                ),
                tags=[NEWS],
                functions=[load_taiga_kp],
            ),
            Meta(
                title='Lenta',
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
                title='Magazines',
                description='Dump of magazines.russ.ru',
                stats=Stats(
                    count=39890,
                    bytes=2352629006
                ),
                functions=[load_taiga_magazines]
            ),
            Meta(
                title='Subtitles',
                stats=Stats(
                    count=19011,
                    bytes=953237022
                ),
                functions=[load_taiga_subtitles]
            ),
            Meta(
                title='Social',
                stats=Stats(
                    count=1876442,
                    bytes=679670941
                ),
                tags=[SOCIAL],
                functions=[load_taiga_social]
            ),
            Meta(
                title='Proza',
                description='Dump of proza.ru',
                stats=Stats(
                    count=1732434,
                    bytes=41067043857
                ),
                tags=[LIT],
                functions=[load_taiga_proza]
            ),
            Meta(
                title='Stihi',
                description='Dump of stihi.ru',
                stats=Stats(
                    count=9157686,
                    bytes=13745805334
                ),
                functions=[load_taiga_stihi]
            ),
        ]
    ),


    #############
    #
    #   BURIY
    #
    ##########


    Group(
        title='Russian NLP Datasets',
        url='https://github.com/buriy/russian-nlp-datasets/releases',
        description='Several Russian news datasets from webhose.io, lenta.ru and other news sites.',
        metas=[
            Meta(
                title='Lenta',
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
                title='News',
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
                title='Webhose',
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
        ]
    ),


    #############
    #
    #    ODS
    #
    #########


    Group(
        title='ODS #proj_news_viz',
        url='https://github.com/ods-ai-ml4sg/proj_news_viz',
        description='Several news sites scraped by members of #proj_news_viz ODS project.',
        metas=[
            Meta(
                title='Interfax',
                description='Dump of interfax.ru.',
                instruction=[
                    'Manually download interfax_v1.csv.zip https://drive.google.com/file/d/1M7z0YoOgpm53IsJ3qOhT_nfiDnGUPeys/view',
                ],
                stats=Stats(
                    count=543962,
                    bytes=1314464670
                ),
                tags=[NEWS],
                functions=[load_ods_interfax],
            ),
            Meta(
                title='Gazeta',
                description='Dump of gazeta.ru.',
                instruction=[
                    'Manually download gazeta_v1.csv.zip from https://drive.google.com/file/d/18B8CvHgmwwyz9GWBZ0TS6dE_x6gYnWCb/view',
                ],
                stats=Stats(
                    count=865847,
                    bytes=1752712439
                ),
                tags=[NEWS],
                functions=[load_ods_gazeta],
            ),
        ]
    )
]
