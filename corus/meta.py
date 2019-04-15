
from .record import Record


class Meta(Record):
    __attributes__ = ['label', 'title', 'source', 'instruction']

    def __init__(self, label, title, source, instruction):
        self.label = label
        self.title = title
        self.source = source
        self.instruction = instruction
