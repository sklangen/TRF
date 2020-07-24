from dataclasses import dataclass, field
from typing import List


@dataclass
class Game(object):
    startrank: int
    color: str
    result: str
    round: int


@dataclass
class Player(object):
    startrank: int
    name: str = ''
    sex: str = 'm'
    title: str = ''
    rating: int = 0
    fed: str = ''
    id: int = None
    birthdate: str = ''
    points: float = 0
    rank: int = None
    games: List[Game] = field(default_factory=list)
