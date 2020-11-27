
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
    __attributes__ = ['entity_id', 'entity_text', 'entity_type', 'start', 'end', 'concept_id', 'concept_name']

    def __init__(self, entity_id, entity_text, entity_type, start, end, concept_id, concept_name):
        self.entity_id = entity_id
        self.entity_text = entity_text
        self.entity_type = entity_type
        self.start = start
        self.end = end
        self.concept_id = concept_id
        self.concept_name = concept_name


def parse_entities(record_entities):
    for entity in record_entities:
        concept_id = entity['concept_id'] if 'concept_id' in entity else ''
        concept_name = entity['concept_name'] if 'concept_name' in entity else ''
        yield RuDReCEntity(
            entity['entity_id'],
            entity['entity_text'],
            entity['entity_type'],
            entity['start'],
            entity['end'],
            concept_id,
            concept_name)


def parse_rudrec(lines):
    records = parse_jsonl(lines)
    for record in records:
        entities = list(parse_entities(record['entities']))
        yield RuDReCRecord(record['file_name'], record['text'], record['sentence_id'], entities)


def load_rudrec(path):
    lines = load_lines(path)
    return parse_rudrec(lines)
