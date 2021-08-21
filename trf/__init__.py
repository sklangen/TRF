from .Entry import ENTRIES
from .Player import Player, Game
from .Tournament import Tournament, Team
import io


def dump(fp, tournament: Tournament):
    '''Dumps the tournament and saves the trf in the file fp points to'''

    _dump_tournament(fp, tournament)


def dumps(tournament: Tournament) -> str:
    '''Dumps the tournament and returns the trf'''

    fp = io.StringIO()
    _dump_tournament(fp, tournament)
    return fp.getvalue()


def load(fp) -> Tournament:
    '''Parses the trf file fp points to and returns it as a tournament'''

    return _parse_tournament(fp.readlines())


def loads(s: str) -> Tournament:
    '''Parses the trf in s and returns it as a tournament'''

    return _parse_tournament(s.split('\n'))


def _dump_tournament(fp, tournament):
    for entry in ENTRIES:
        entry.dump(fp, tournament)

    for field, value in tournament.xx_fields.items():
        fp.write(f'{field} {value}\n')


def _parse_tournament(lines):
    tournament = Tournament()

    for line in lines:
        for entry in ENTRIES:
            if line.startswith(entry.din + ' '):
                entry.load(tournament, line[4:])
                break

        if line.startswith('XX'):
            field, value = line.split(' ', 1)
            tournament.xx_fields[field] = value.strip()

    return tournament
