# coding: utf8

import re
from itertools import islice as head

from corus.record import Record
from corus.io import match_names

from .common import (
    load_tar,
    parse_filename_id
)


FB = 'fb'
LJ = 'lj'
TWITTER = 'twitter'
VK = 'vk'
NETWORKS = {
    'fbtexts': FB,
    'LiveJournalPostsandcommentsGICR': LJ,
    'twtexts': TWITTER,
    'vktexts': VK
}


class TaigaSocialRecord(Record):
    __attributes__ = ['id', 'network', 'text']

    def __init__(self, id, network, text):
        self.id = id
        self.network = network
        self.text = text


def parse_lines(file, encoding='utf8'):
    for line in file:
        line = line.decode(encoding)
        yield line.lstrip('\ufeff').rstrip('\r\n')


def parse_lj(file):
    for text in parse_lines(file):
        yield TaigaSocialRecord(
            id=None,
            network=LJ,
            text=text
        )


# DataBaseItem: 6_5756d99b5dd2dc3dac164155
# Кстати, как неожиданно КПРФ
# DataBaseItem: 6_5756d9a85dd2dc3dac1645ae
# [id12890229|Евгений], можно и по-другому сказать: "убогая клоунада" КПРФ - это


def flush(network, id, buffer):
    text = '\n'.join(buffer)
    return TaigaSocialRecord(
        id=id,
        network=network,
        text=text
    )


def parse_social_(file, network):
    lines = parse_lines(file)
    previous = None
    buffer = []
    for line in lines:
        match = re.match(r'^DataBaseItem: (.+)$', line)
        if match:
            if previous:
                yield flush(network, previous, buffer)
                buffer = []
            previous = match.group(1)
        else:
            buffer.append(line)
    if previous:
        yield flush(network, previous, buffer)
        buffer = []


def parse_social(file, network):
    if network == LJ:
        return parse_lj(file)
    else:
        return parse_social_(file, network)


def load_taiga_social(path, offset=3985892864, count=4):
    records = load_tar(path, offset=offset)
    records = match_names(records, '*/texts/*.txt')
    records = head(records, count)
    for record in records:
        network = parse_filename_id(record.name)
        network = NETWORKS[network]
        for record in parse_social(record.file, network):
            yield record


__all__ = [
    'load_taiga_social'
]
