from abc import ABC, abstractmethod
from .Player import Player, Game
from .Tournament import Team
from .TrfException import TrfException
import re


class TrfEntry(ABC):
    def __init__(self, din):
        self.din = din

    @abstractmethod
    def dump(self, fp, tournament):
        pass

    @abstractmethod
    def load(self, tournament, data):
        pass


class SingleLineEntry(TrfEntry):
    def __init__(self, din, fieldname):
        super().__init__(din)
        self.fieldname = fieldname

    def dump(self, fp, tournament):
        value = tournament.__dict__[self.fieldname]
        fp.write(f'{self.din} {self.format(value)}\n')

    def format(self, value):
        return str(value)

    def load(self, tournament, data):
        value = self.parse(data.strip())
        tournament.__dict__[self.fieldname] = value

    def parse(self, data):
        return data


class SingleLineIntEntry(SingleLineEntry):
    def __init__(self, din, fieldname):
        super().__init__(din, fieldname)

    def parse(self, data):
        return int(data)


class SingleLineListEntry(SingleLineEntry):
    def __init__(self, din, fieldname, delim):
        super().__init__(din, fieldname)
        self.delim = delim

    def dump(self, fp, tournament):
        value = tournament.__dict__[self.fieldname]
        data = self.delim.join(self.format(v) for v in value)
        fp.write(f'{self.din} {data}\n')

    def load(self, tournament, data):
        value = [self.parse(s) for s in data.strip().split(self.delim) if s]
        tournament.__dict__[self.fieldname] = value


PLAYER_LINE_PATTERN = re.compile(r'^(?P<startrank>[ \d]{4}) (?P<sex>[\w ]) (?P<title>[\w ]{2}) (?P<name>.{33}) (?P<rating>[ \d]{4}) (?P<fed>[\w ]{3}) (?P<id>[ \d]{11}) (?P<birthdate>.{10}) (?P<points>[ \d.]{4}) (?P<rank>[ \d]{4})(?P<games>(  [ \d]{4} [bsw\- ] [1=0+wdl\-hfuz ]| {10})*)\s*$', re.IGNORECASE)


class PlayerEntry(TrfEntry):
    def __init__(self):
        super().__init__('001')

    def dump(self, fp, tournament):
        for player in tournament.players:
            self.dump_player(fp, player)
            fp.write('\n')

    def dump_player(self, fp, player):
        fp.write('001')
        fp.write(f' {player.startrank:>4}')
        fp.write(f' {player.sex:1}')
        fp.write(f' {player.title:>2}')
        fp.write(f' {player.name:<33}')
        fp.write(f' {player.rating or "":>4}')
        fp.write(f' {player.fed:<3}')
        fp.write(f' {player.id or "":>11}')
        fp.write(f' {player.birthdate:>10}')
        fp.write(f' {player.points:>4}')
        fp.write(f' {"" if player.rank is None else player.rank:>4}')

        for game in player.games:
            sr = '0000' if game.startrank == 0 else game.startrank or ''
            fp.write(f'  {sr:>4} {game.color:1} {game.result:1}')

    def load(self, tournament, data):
        match = PLAYER_LINE_PATTERN.fullmatch(data)
        if match is None:
            raise TrfException(f'Player data not matching pattern: {data}')

        player = Player(
            startrank=int(match.group('startrank')),
            sex=match.group('sex'),
            title=match.group('title').strip(),
            name=match.group('name').strip(),
            rating=int_or_default(match.group('rating'), 0),
            fed=match.group('fed').strip(),
            id=int_or_default(match.group('id')),
            birthdate=match.group('birthdate').strip(),
            points=float(match.group('points')),
            rank=int_or_default(match.group('rank')),
            games=list(self.parse_games(match.group('games')[2:].rstrip()))
        )
        tournament.players.append(player)

    def parse_games(self, string):
        round = 1
        while len(string) >= 8:
            yield Game(
                startrank=int_or_default(string[:4].strip()),
                color=string[5],
                result=string[7],
                round=round
            )
            round += 1
            string = string[10:]


def int_or_default(string, default=None):
    if string == '' or string.isspace():
        return default
    return int(string)


class TeamEntry(TrfEntry):
    def __init__(self):
        super().__init__('013')

    def dump(self, fp, tournament):
        for team in tournament.teams:
            startranks = ' '.join(f'{s:>4}' for s in team.startranks)
            fp.write(f'013 {team.name:32} {startranks}\n')

    def load(self, tournament, data):
        name = data[:32].strip()
        startranks = [int(s) for s in data[32:].strip().split() if s]
        tournament.teams.append(Team(name, startranks))


ENTRIES = [
    SingleLineEntry('012', 'name'),
    SingleLineEntry('022', 'city'),
    SingleLineEntry('032', 'federation'),
    SingleLineEntry('042', 'startdate'),
    SingleLineEntry('052', 'enddate'),
    SingleLineIntEntry('062', 'numplayers'),
    SingleLineIntEntry('072', 'numratedplayers'),
    SingleLineIntEntry('082', 'numteams'),
    SingleLineEntry('092', 'type'),
    SingleLineEntry('102', 'chiefarbiter'),
    SingleLineEntry('112', 'deputyarbiters'),
    SingleLineEntry('122', 'rateofplay'),
    SingleLineListEntry('132', 'rounddates', delim=' '),
    TeamEntry(),
    PlayerEntry()
]
