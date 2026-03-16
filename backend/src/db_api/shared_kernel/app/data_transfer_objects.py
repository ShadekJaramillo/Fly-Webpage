from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Level(str, Enum):
  ROOKIE = "rookie"
  WARRIOR = "warrior"
  NINJA = "ninja"


class Athlete(BaseModel):
  uuid: UUID
  first_name: str
  second_name: str
  level: Level
