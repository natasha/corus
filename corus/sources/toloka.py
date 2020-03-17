
from corus.record import Record
from corus.io import (
    load_lines,
    parse_tsv,
    skip_header
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
