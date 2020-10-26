
from corus.record import Record
from corus.io import (
    load_lines,
    parse_tsv,
    skip_header,
    rstrip
)


class LRWCRecord(Record):
    __attributes__ = ['hyponym', 'hypernym', 'genitive', 'judgement', 'confidence']

    def __init__(self, hyponym, hypernym, genitive, judgement, confidence):
        self.hyponym = hyponym
        self.hypernym = hypernym
        self.genitive = genitive
        self.judgement = judgement
        self.confidence = confidence


# INPUT:hyponym   INPUT:hypernym  INPUT:genitive  OUTPUT:judgement        CONFIDENCE:judgement
# автомобиль      автомашина      автомашины      true    99.75%
# автомобиль      автомототранспорт       автомототранспорта      true    99.96%
# автомобиль      автомототранспортный    автомототранспортного   true    99.99%


def parse_judgement(value):
    if value == 'true':
        return 1.0
    elif value == 'false':
        return 0.0


def parse_confidence(value):
    return float(value[:-1])


def parse_toloka_lrwc(lines):
    skip_header(lines)
    records = parse_tsv(lines)
    for record in records:
        hyponym, hypernym, genitive, judgement, confidence = record
        judgement = parse_judgement(judgement)
        confidence = parse_confidence(confidence)
        yield LRWCRecord(hyponym, hypernym, genitive, judgement, confidence)


def load_toloka_lrwc(path):
    lines = load_lines(path)
    return parse_toloka_lrwc(lines)


class RuADReCTRecord(Record):
    __attributes__ = ['tweet_id', 'tweet', 'label']

    def __init__(self, tweet_id, tweet, label):
        self.tweet_id = tweet_id
        self.tweet = tweet
        self.label = label

# – tweet_id: уникальный номер сообщения в системе twitter;
# – tweet:  текст сообщения (твита);
# - label: класс твита, 1 - содержит упоминание побочного эффекта, 0 - не содердит


def parse_ruadrect(lines):
    rows = parse_tsv(lines)
    skip_header(rows)
    for cells in rows:
        yield RuADReCTRecord(*cells)


def load_lines_ruadrect(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            yield rstrip(line)


def load_ruadrect(path):
    lines = load_lines_ruadrect(path)
    return parse_ruadrect(lines)
