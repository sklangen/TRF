from .Player import Player
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Team(object):
    name: str = ''
    startranks: List[int] = field(default_factory=list)


@dataclass
class Tournament(object):
    name: str = ''
    city: str = ''
    federation: str = ''
    startdate: str = ''
    enddate: str = ''
    numplayers: int = 0
    numratedplayers: int = 0
    numteams: int = 0
    type: str = ''
    chiefarbiter: str = ''
    deputyarbiters: str = ''
    rateofplay: str = ''
    rounddates: List[str] = field(default_factory=list) 
    players: List[Player] = field(default_factory=list) 
    teams: List[str] = field(default_factory=list) 
    xx_fields: Dict[str, str] = field(default_factory=dict)

    @property
    def numrounds(self):
        '''An estemation of how many rounds where played in this tournament.'''

        if 'XXR' in self.xx_fields:
            return int(self.xx_fields['XXR'])

        if self.rounddates:
            return len(self.rounddates)

        return max(len(p.games) for p in self.players) or len(self.players)-1
