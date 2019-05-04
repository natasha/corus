# coding: utf8

import re
from datetime import datetime

from corus.record import Record
from corus.io import load_lines


# – id: уникальный номер сообщения в системе twitter;
# – tdate: дата публикации сообщения (твита);
# – tmane: имя пользователя, опубликовавшего сообщение;
# – ttext:  текст сообщения (твита);
# – ttype: поле в котором в дальнейшем будет указано к кому классу относится твит (положительный, отрицательный, нейтральный);
# – trep: количество реплаев к данному сообщению. В настоящий момент API твиттера не отдает эту информацию;
# – tfav: число сколько раз данное сообщение было добавлено в избранное другими пользователями;
# – tstcount: число всех сообщений пользователя в сети twitter;
# – tfol: количество фоловеров пользователя (тех людей, которые читают пользователя);
# – tfrien: количество друзей пользователя (те люди, которых читает пользователь);
# – listcount: количество листов-подписок в которые добавлен твиттер-пользователь.


class MokoronRecord(Record):
    __attributes__ = [
        'id', 'timestamp', 'user', 'text', 'sentiment',
        'replies', 'retweets', 'favourites', 'posts',
        'followers', 'friends', 'lists'
    ]

    def __init__(self, id, timestamp, user, text, sentiment,
                 replies, retweets, favourites, posts, followers, friends, lists):
        self.id = id
        self.timestamp = timestamp
        self.user = user
        self.text = text
        self.sentiment = sentiment
        self.replies = replies
        self.retweets = retweets
        self.favourites = favourites
        self.posts = posts
        self.followers = followers
        self.friends = friends
        self.lists = lists

    @classmethod
    def from_match(cls, match):
        dict = match.groupdict()
        for key in ['id', 'sentiment', 'replies', 'retweets',
                    'favourites', 'posts', 'followers', 'friends', 'lists']:
            dict[key] = int(dict[key])
        dict['timestamp'] = datetime.utcfromtimestamp(float(dict['timestamp']))
        return cls(**dict)


# INSERT INTO `sentiment` VALUES (408906695721877504,'1386325928','Va5ilina','Пропавшая в Хабаровске школьница почти сутки провела в яме у коллектор',2,0,0,0,183,95,158,0),(408906695700520960,'1386325928','i_wont_judge_ya','ЛЕНТА, Я СЕГОДНЯ ПОЛГОДА ДИРЕКШИОНЕЕЕЕР! С:\nХОТЯ ВСЕ РАВНО НИКТО НЕ ПОЗДРАВИТ ЛОЛ',2,0,0,0,19809,804,257,11),


INSERT = 'INSERT INTO `sentiment` VALUES'
RECORD = re.compile(r'''
\(
  (?P<id>\d+),
  '(?P<timestamp>\d+)',
  '(?P<user>.+?)',
  '(?P<text>.+?)',
  (?P<sentiment>\d+),
  (?P<replies>\d+),
  (?P<retweets>\d+),
  (?P<favourites>\d+),
  (?P<posts>\d+),
  (?P<followers>\d+),
  (?P<friends>\d+),
  (?P<lists>\d+)
\)
''', re.X)


def load_mokoron(path):
    for line in load_lines(path):
        if line.startswith(INSERT):
            for match in RECORD.finditer(line):
                yield MokoronRecord.from_match(match)


__all__ = [
    'load_mokoron'
]
