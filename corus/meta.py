
from .record import Record


class Meta(Record):
    __attributes__ = ['label', 'title', 'source', 'description', 'instruction']

    def __init__(self, label, title, source, description, instruction):
        self.label = label
        self.title = title
        self.source = source
        self.description = description
        self.instruction = instruction
