from typing import TypedDict

from pydantic import BaseModel


class Game(TypedDict):
    id: int
    name: str
    yearPublished: int
    difficulty: int
    avgRating: int
    minPlayers: int
    maxPlayers: int
    playtime: int
    minAge: int
    image: str


class PagedRequest(BaseModel):
    offset: int
    limit: int


class GamesResponse(TypedDict):
    games: list[Game]
    totalNumberOfGames: int
