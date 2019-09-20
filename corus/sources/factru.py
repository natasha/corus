# coding: utf8

import re
from corus.path import (
    list_dir,
    join_path
)
from corus.record import Record
from corus.io import (
    load_text,
    load_lines,
)


DEVSET = 'devset'
TESTSET = 'testset'

TXT = 'txt'
SPANS = 'spans'
OBJECTS = 'objects'
COREF = 'coref'
FACTS = 'facts'


class FactruSpan(Record):
    __attributes__ = ['id', 'type', 'start', 'stop']

    def __init__(self, id, type, start, stop):
        self.id = id
        self.type = type
        self.start = start
        self.stop = stop


class FactruObject(Record):
    __attributes__ = ['id', 'type', 'spans']

    def __init__(self, id, type, spans):
        self.id = id
        self.type = type
        self.spans = spans


class FactruCorefSlot(Record):
    __attributes__ = ['type', 'value']

    def __init__(self, type, value):
        self.type = type
        self.value = value


class FactruCoref(Record):
    __attributes__ = ['id', 'objects', 'slots']

    def __init__(self, id, objects, slots):
        self.id = id
        self.objects = objects
        self.slots = slots


class FactruFactSlot(Record):
    __attributes__ = ['type', 'value']

    def __init__(self, type, value):
        self.type = type
        self.value = value


class FactruFact(Record):
    __attributes__ = ['id', 'type', 'slots']

    def __init__(self, id, type, slots):
        self.id = id
        self.type = type
        self.slots = slots


class FactruMarkup(Record):
    __attributes__ = ['id', 'text', 'facts']

    def __init__(self, id, text, facts):
        self.id = id
        self.text = text
        self.facts = facts


def list_ids(dir, set):
    for filename in list_dir(join_path(dir, set)):
        match = re.match(r'^book_(\d+)\.txt$', filename)
        if match:
            yield match.group(1)


def part_path(id, dir, set, part):
    return join_path(dir, set, 'book_%s.%s' % (id, part))


def parse_spans(lines):
    # 32962 loc_name 17 6 89971 1  # 89971 Италии
    # 32963 org_name 26 4 89973 1  # 89973 миде
    # 32965 loc_name 31 6 89974 1  # 89974 Грузии

    for line in lines:
        id, type, start, size, _ = line.split(None, 4)
        start = int(start)
        stop = start + int(size)
        yield FactruSpan(id, type, start, stop)


def parse_objects(lines, spans):
    # 16972 LocOrg 32962 # Италии
    # 16975 Org 32963 32965 # миде Грузии

    id_spans = {_.id: _ for _ in spans}
    for line in lines:
        parts = iter(line.split())
        id = next(parts)
        type = next(parts)
        spans = []
        for index in parts:
            if not index.isdigit():
                break
            span = id_spans[index]
            spans.append(span)
        yield FactruObject(id, type, spans)


def parse_coref_slots(lines):
    for line in lines:
        if not line:
            break

        parts = line.split(None, 1)
        if len(parts) == 1:
            # 1101 18638 18654
            # name Венгрия
            # wikidata
            # lastname
            continue

        type, value = parts
        yield FactruCorefSlot(type, value)


def parse_corefs(lines, objects):
    # 3 16968 16970 16974
    # name Грузия
    #
    # 5 16969
    # firstname Виторио
    # lastname Сандали

    id_objects = {_.id: _ for _ in objects}
    for line in lines:
        parts = iter(line.split())
        id = next(parts)
        objects = [id_objects[_] for _ in parts]
        slots = list(parse_coref_slots(lines))
        yield FactruCoref(id, objects, slots)


def parse_facts_slots(lines, id_corefs, id_spans):
    for line in lines:
        if not line:
            break
        type, line = line.split(None, 1)
        values = line.split(' | ')
        for value in values:
            # Participant obj90 Industrial and Commercial Bank of China | Промышленный и коммерческий банк Китая
            # Participant obj3640 WhatsApp
            # Type купля/продажа
            match = re.search(r'^(obj|span)(\d+)', value)
            if match:
                section, id = match.groups()
                if section == 'obj':
                    value = id_corefs[id]
                elif section == 'span':
                    value = id_spans[id]

            yield FactruFactSlot(type, value)


def parse_facts(lines, corefs, spans):
    # 58-0 Meeting
    # Participant obj5 Сандали Виторио
    # Participant obj6 Налбандов Александр
    #
    # 58-1 Occupation
    # Who obj5 Сандали Виторио
    # Where obj2 Италия
    # Position span32958 чрезвычайный и полномочный посол | span64007 чрезвычайный и полномочный посол Италии в Грузии

    id_corefs = {_.id: _ for _ in corefs}
    id_spans = {_.id: _ for _ in spans}
    for line in lines:
        id, type = line.split(None, 1)
        slots = list(parse_facts_slots(lines, id_corefs, id_spans))
        yield FactruFact(id, type, slots)


def load_id(id, dir, set):
    path = part_path(id, dir, set, TXT)
    text = load_text(path)

    path = part_path(id, dir, set, SPANS)
    lines = load_lines(path)
    spans = list(parse_spans(lines))

    path = part_path(id, dir, set, OBJECTS)
    lines = load_lines(path)
    objects = list(parse_objects(lines, spans))

    path = part_path(id, dir, set, COREF)
    lines = load_lines(path)
    corefs = list(parse_corefs(lines, objects))

    path = part_path(id, dir, set, FACTS)
    lines = load_lines(path)
    facts = list(parse_facts(lines, corefs, spans))

    return FactruMarkup(id, text, facts)


def load_factru(dir, sets=[DEVSET, TESTSET]):
    for set in sets:
        for id in list_ids(dir, set):
            yield load_id(id, dir, set)
