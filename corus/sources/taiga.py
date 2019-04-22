
import re
from itertools import islice as head
from datetime import datetime

from ..record import Record
from ..path import (
    get_filename,
    split_ext
)
from ..io import (
    open_tar,
    list_tar,
    match_names,
    read_tar,
    parse_tsv,
    skip_header
)


class TaigaRecord(Record):
    __attributes__ = ['meta', 'text']

    def __init__(self, meta, text):
        self.meta = meta
        self.text = text


########
#
#   META
#
#########


class Meta(Record):
    __attributes__ = ['id', 'timestamp', 'tags', 'themes', 'rubric',
                      'author', 'lang', 'title', 'url']

    def __init__(self, id, timestamp=None, tags=(), themes=(), rubric=None,
                 author=None, lang=None, title=None, url=None):
        self.id = id
        self.timestamp = timestamp
        self.tags = tags
        self.themes = themes
        self.rubric = rubric
        self.author = author
        self.lang = lang
        self.title = title
        self.url = url


def parse_meta(text):
    lines = iter(text.splitlines())
    rows = parse_tsv(lines)
    header = skip_header(rows)
    for row in rows:
        yield dict(zip(header, row))


def load_metas(path, pattern, count):
    with open_tar(path) as tar:
        members = list_tar(tar)
        members = match_names(members, pattern)
        members = head(members, count)
        for member in members:
            text = read_tar(tar, member)
            for item in parse_meta(text):
                yield item


##########
#
#   TEXTS
#
#######


def load_texts(path, pattern='*/texts/*.txt'):
    with open_tar(path) as tar:
        members = list_tar(tar)
        members = match_names(members, pattern)
        for member in members:
            yield member.name, read_tar(tar, member)


##############
#
#   ARZAMAS
#
##########


# {'About_author': '',
#  'Author_profession': 'Кандидат исторических наук. Креативный директор Фонда Егора Гайдара. Один из\xa0участников сетевого проекта «Прожито», создающего полный электронный корпус дневников советского времени.',
#  'URL': 'http://arzamas.academy/mag/427-chapter7Историк советской литературы и\xa0культуры',
#  'author': 'Илья Венявкин',
#  'id': '427',
#  'source': 'Arzamas',
#  'tags': "['Документ', 'СССР']",
#  'textdate': '27.04.2017',
#  'theme': "['Литература', 'История']",
#  'title': 'Советский писатель внутри Большого террора. Глава 7  •  '}


def parse_arzamas_metas(items):
    for item in items:
        id = item['id']
        timestamp = datetime.strptime(item['textdate'], '%d.%m.%Y')
        tags = eval(item['tags'])
        themes = eval(item['theme'])
        author = item['author']
        title = item['title']
        url = item['URL']
        yield id, Meta(
            id=id,
            timestamp=timestamp,
            tags=tags,
            themes=themes,
            author=author,
            title=title,
            url=url
        )


# home/tsha/Arzamas/texts/arzamas_449.txt
# home/tsha/Arzamas/texts/arzamas_450.txt
# home/tsha/Arzamas/texts/arzamas_452.txt


def parse_arzamas_id(name):
    match = re.search(r'arzamas_(\d+)\.txt', name)
    return match.group(1)


def load_taiga_arzamas(path):
    items = load_metas(path, '*/metatable.csv', 1)
    metas = dict(parse_arzamas_metas(items))
    for name, text in load_texts(path):
        id = parse_arzamas_id(name)
        meta = metas[id]
        yield TaigaRecord(meta, text)


########
#
#   FONTANKA
#
########


# {'author': '',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '04.04.2015',
#   'magazine': '',
#   'segment': 'Fontanka',
#   'tags': 'Санкт-Петербург, Петербург, СПб, фонтанка, фонтанка.ру, АЖУР, Агентство Журналистских расследований, СМИ, новости, новости Петербурга, политика, экономика, криминал, Фонтанка, информация, события, город, культура,  политика,  бизнес,  общество,  происшествия,  спорт, свободное время, авто, недвижимость, зарубежная недвижимость, Охта центр, финансы, туризм, работа, особое мнениеhttp://www.fontanka.ru/2015/04/04/068/',
#   'textdiff': '',
#   'textid': '20150404068',
#   'textname': 'Минобороны: Россия не отстает от США в разработке лазерного оружия',
#   'textregion': '',
#   'textrubric': 'Технологии',
#   'time': '20:59'},


def parse_fontanka_metas(items):
    for item in items:
        id = item['textid']
        # {'segment': 'Fontanka', 'textname': '&quot;', 'textid': '20100205145'}
        tags, url, rubric, author, title = (), None, None, None, None

        if 'date' in item and 'time' in item:
            timestamp = item['date'] + item['time']
            if timestamp:
                timestamp = datetime.strptime(timestamp, '%d.%m.%Y%H:%M')

        if 'tags' in item:
            tags = item['tags']
            match = re.search(r'(http://.+)$', tags)
            if match:
                url = match.group(1)
                tags = re.split(r',\s+', tags[:match.start()])

        rubric = item.get('textrubric')
        author = item.get('author')
        title = item.get('textname')
        yield id, Meta(
            id=id,
            timestamp=timestamp,
            tags=tags,
            rubric=rubric,
            author=author,
            title=title,
            url=url
        )


# home/tsha/Fontanka/texts/2007/fontanka_20070101001.txt
# home/tsha/Fontanka/texts/2007/fontanka_20070101002.txt
# home/tsha/Fontanka/texts/2007/fontanka_20070101004.txt
# home/tsha/Fontanka/texts/2007/fontanka_20070101003.txt


def parse_fontanka_id(name):
    match = re.search(r'fontanka_(\d+)\.txt', name)
    return match.group(1)


def load_taiga_fontanka(path):
    items = load_metas(path, '*/metatable_*.csv', 2017 - 2005 + 1)
    metas = dict(parse_fontanka_metas(items))
    for name, text in load_texts(path):
        id = parse_fontanka_id(name)
        meta = metas[id]
        yield TaigaRecord(meta, text)


########
#
#   INTERFAX
#
########


# {'author': '',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '2013-02-24',
#   'magazine': '',
#   'segment': 'Interfax',
#   'source': 'http://www.interfax.ru/russia/292151',
#   'tags': 'Кубань',
#   'textdiff': '',
#   'textid': 'russia292151',
#   'textname': '60 тысяч жителей Туапсинского района остались без электричества',
#   'textregion': '',
#   'textrubric': 'В России',
#   'time': '16:10'},


def parse_interfax_metas(items):
    for item in items:
        id = item['textid']

        timestamp = item['date'] + item['time']
        try:
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d%H:%M')
        except ValueError:
            # rare, date='' time='2011-09-12'
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d')

        title = item['textname']
        tags = item['tags']
        author = item['author']
        rubric = item.get('rubric')
        url = item['source']
        yield id, Meta(
            id=id,
            timestamp=timestamp,
            title=title,
            rubric=rubric,
            tags=tags,
            author=author,
            url=url
        )


# home/tsha/Interfax/texts/business225067.txt
# home/tsha/Interfax/texts/business225113.txt
# home/tsha/Interfax/texts/business225178.txt


def parse_filename_id(path):
    id, _ = split_ext(get_filename(path))
    return id


parse_interfax_id = parse_filename_id


def load_taiga_interfax(path):
    items = load_metas(path, '*/newmetadata.csv', 1)
    metas = dict(parse_interfax_metas(items))
    for name, text in load_texts(path):
        id = parse_interfax_id(name)
        meta = metas[id]
        yield TaigaRecord(meta, text)


############
#
#    KP
#
##########


# {'author': 'Мария ГОШИНА',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '2017-01-20',
#   'magazine': '',
#   'segment': 'KP',
#   'source': 'http://www.kp.ru/online/news/2632060/',
#   'tags': '',
#   'textdiff': '',
#   'textid': '10@2632060',
#   'textname': 'В Саратове спасатели помогли родственникам попасть в квартиру пенсионерки',
#   'textregion': 'www.saratov.kp.ru',
#   'textrubric': 'Общество>Общество',
#   'time': '09:27:00+03:00'},


def parse_kp_metas(items):
    for item in items:
        id = item['textid']
        yield id, Meta(
            id=id
        )


# home/tsha/KP/texts/10@2598286.txt
# home/tsha/KP/texts/10@2598287.txt
# home/tsha/KP/texts/10@2598289.txt


parse_kp_id = parse_filename_id


def load_taiga_kp(path):
    items = load_metas(path, '*/newmetadata.csv', 1)
    metas = dict(parse_kp_metas(items))
    for name, text in load_texts(path):
        id = parse_kp_id(name)
        meta = metas[id]
        yield TaigaRecord(meta, text)


############
#
#   LENTA
#
##########


# {'author': '',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '8 марта 2011',
#   'magazine': '',
#   'segment': 'Lenta',
#   'source': 'https://lenta.ru/news/2011/03/08/hobgoblin/',
#   'tags': '',
#   'textdiff': '',
#   'textid': '20110308hobgoblin',
#   'textname': 'HBO запустит сериал о волшебной войне с Гитлером',
#   'textregion': '',
#   'textrubric': 'Культура',
#   'time': '14:33'},


def parse_lenta_metas(items):
    for item in items:
        id = item['textid']
        yield id, Meta(
            id=id
        )


# home/tsha/Lenta/texts/20100101three.txt
# home/tsha/Lenta/texts/20100101tomsk.txt
# home/tsha/Lenta/texts/20100101urus.txt


parse_lenta_id = parse_filename_id


def load_taiga_lenta(path):
    items = load_metas(path, '*/newmetadata.csv', 1)
    metas = dict(parse_lenta_metas(items))
    for name, text in load_texts(path):
        id = parse_lenta_id(name)
        if id not in metas:
            # rare: 20120904e95, 20141007conscription
            meta = Meta(id=id)
        else:
            meta = metas[id]
        yield TaigaRecord(meta, text)


#########
#
#    N+1
#
###########


# {'author': 'Владимир Королев',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '21 Янв. 2017',
#   'magazine': '',
#   'segment': 'nplus1',
#   'source': 'https://nplus1.ru/news/2017/01/21/Asphaltene-3d',
#   'tags': '',
#   'textdiff': '5.2',
#   'textid': '20170121Asphaltene-3d',
#   'textname': '«Архипелаги» асфальтенов ощупали в 3D',
#   'textregion': '',
#   'textrubric': 'Наука',
#   'time': '17:34'},


def parse_nplus1_metas(items):
    for item in items:
        id = item['textid']
        yield id, Meta(
            id=id
        )


# home/tsha/NPlus1/texts/20150320drone.txt
# home/tsha/NPlus1/texts/20150320nitrogen.txt
# home/tsha/NPlus1/texts/20150320silica.txt


parse_nplus1_id = parse_filename_id


def load_taiga_nplus1(path):
    items = load_metas(path, '*/newmetadata.csv', 1)
    metas = dict(parse_nplus1_metas(items))
    for name, text in load_texts(path):
        id = parse_nplus1_id(name)
        meta = metas[id]
        yield TaigaRecord(meta, text)


############
#
#   MAGAZINES
#
########


# {'author': '',
#   'authorreaders': '',
#   'authortexts': '',
#   'date': '2007, 10',
#   'magazine': 'Знамя',
#   'segment': 'Журнальный зал',
#   'source': 'http://magazines.russ.ru/znamia/2007/10/tu26.html',
#   'tags': '',
#   'textdiff': '',
#   'textid': '50005',
#   'textname': 'Михаил Копелиович. Рецензия &amp;#8211; любовь моя',
#   'textregion': '',
#   'textrubric': 'article',
#   'time': ''},


def parse_magazines_metas(items):
    for item in items:
        id = item.get('textid')
        if not id:
            continue

        url = None
        if 'source' in item:
            url = item['source']
            match = re.search(r'russ\.ru/([^/]+)', url)
            label = match.group(1)
            id = label + '_' + id
        yield id, Meta(
            id=id,
            url=url
        )


# home/tsha/Magazines/texts/corpus_arion_10658.txt
# home/tsha/Magazines/texts/corpus_arion_10659.txt


def parse_magazines_id(name):
    match = re.search(r'corpus_([\d\w_]+)\.txt', name)
    if not match:
        print(name)
    return match.group(1)


def load_taiga_magazines(path):
    items = load_metas(path, '*/corpus_*_metadata.csv', 36)
    metas = dict(parse_magazines_metas(items))
    for name, text in load_texts(path):
        id = parse_magazines_id(name)
        if id in metas:
            meta = metas[id]
        else:
            # rare when url not in meta
            meta = Meta(id=id)
        yield TaigaRecord(meta, text)


###########
#
#   SUBTITLES
#
#########


# [{'filepath': 'Heroes - 3x12 - Our Father.HDTV.LOL.en.txt',
#   'id': '8940',
#   'languages': 'en',
#   'title': 'Heroes - 3x12 - Our Father.HDTV.LOL.en.srt'},
#  {'filepath': 'Friends - 3x17 - The One Without The Ski Trip.ru.txt',
#   'id': '7553',
#   'languages': 'ru',
#   'title': 'Friends - 3x17 - The One Without The Ski Trip.ru.srt'},


def parse_subtitles_metas(items):
    for item in items:
        id = parse_filename_id(item['filepath'])
        lang = item['languages']
        title = item['title']
        yield id, Meta(
            id=id,
            lang=lang,
            title=title
        )


# home/tsha/Subtitles/texts/12 Monkeys/12 Monkeys - 1x01 - Splinter.HDTV.KILLERS.en.txt
# home/tsha/Subtitles/texts/12 Monkeys/12 Monkeys - 1x01 - Splinter.HDTV.KILLERS.ru.txt


parse_subtitles_id = parse_filename_id


def load_taiga_subtitles(path):
    items = load_metas(path, '*/metatable.csv', 1)
    metas = dict(parse_subtitles_metas(items))
    for name, text in load_texts(path):
        id = parse_subtitles_id(name)
        if id in metas:
            meta = metas[id]
        else:
            # rare 'Survivors - 1x06 - Episode 6.it'
            meta = Meta(id=id)
        yield TaigaRecord(meta, text)
