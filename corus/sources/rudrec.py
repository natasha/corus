
from corus.record import Record
from corus.io import (
    parse_jsonl,
    load_lines
)


class RuDReCRecord(Record):
    __attributes__ = ['file_name', 'text', 'sentence_id', 'entities']

    def __init__(self, file_name, text, sentence_id, entities):
        self.file_name = file_name
        self.text = text
        self.sentence_id = sentence_id
        self.entities = entities


class RuDReCEntity(Record):
    __attributes__ = [
        'entity_id', 'entity_text', 'entity_type',
        'start', 'end', 'concept_id', 'concept_name'
    ]

    def __init__(self, entity_id, entity_text, entity_type, start, end, concept_id, concept_name):
        self.entity_id = entity_id
        self.entity_text = entity_text
        self.entity_type = entity_type
        self.start = start
        self.end = end
        self.concept_id = concept_id
        self.concept_name = concept_name


def parse_entities(items):
    for item in items:
        yield RuDReCEntity(
            item['entity_id'],
            item['entity_text'],
            item['entity_type'],
            item['start'],
            item['end'],
            item.get('concept_id'),
            item.get('concept_name')
        )


def parse_rudrec(items):
    for item in items:
        entities = list(parse_entities(item['entities']))
        yield RuDReCRecord(
            item['file_name'],
            item['text'],
            item['sentence_id'],
            entities
        )


def load_rudrec(path):
    lines = load_lines(path)
    items = parse_jsonl(lines)
    return parse_rudrec(items)
