from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Collection


@dataclass
class DateRange:
  start: datetime
  finish: datetime


class UserAccess(Enum):
  ADMIN = "admin"
  TRAINER = "trainer"
  ATHLETE = "athlete"


@dataclass
class AuthenticatedUser:
  """
  Represents the information of a requester to the app.

  Attributes:
    id (int): Unique identifier of the user making the request.
    access (UserAccess): Level of access granted to the user.
  """

  id: int
  access: UserAccess


class ChineseLevel(Enum):
  ROOKIE = 1
  WARRIOR = 2
  NINJA = 3


@dataclass
class FullName:
  first_name: str
  second_name: str


# TODO first we need to decide about how to authenticate users.
# @dataclass
# class VolatileUser:


@dataclass
class VolatileAthlete:
  """
  Class for athletes not registered to the database yet.
  Attributes:

    trainer_id (int): Unique identifier of the trainer assigned to the
      athlete.
    full_name (FullName): Athlete's full name.
    athlete_level (ChineseLevel): Athlete's pole sport level according to the
      Chinese methodology.
    date_joined (datetime): Date the athlete became a client.
  """

  trainer_id: int
  full_name: FullName
  athlete_level: ChineseLevel
  date_joined: datetime


@dataclass
class VolatileTrainer:
  full_name: FullName
  trainer_level: ChineseLevel
  date_joined: datetime


# IMPORTANT NOTE: Although PersistedAthlete and PersistedTrainer classes are
# implemented in the this module, the reccomended approach is to implement
# custom classes on each module that contain only the required fields for the
# module operations and then cast PersistedAthlete and PersistedTrainer
# instances fetched from its respective port, into these custom classes. For the
# ports in these modules they should use the ports in `shared_kernel.adapters`
# as dependencies. This apporach is more verbose but prevents modules from using
# instances with attributes that may or may not be None, forcing modules to make
# checks for their specific use cases and to implement tests on the adapters to
# make sure the returned object passes the check.


@dataclass
class PersonName:
  first_name: str | None
  second_name: str | None


@dataclass
class PersistedAthlete:
  """
  Represents an athlete fetched from a repository.

  Attributes:
    id (int): Internal unique identifyer of the athlete.
    user_id (int): Internal unique identifyer of athlete's user.
    trainer_id (int): Internal unique identifyer of athlete's trainer.
    name (PersonName | None): Athlete's full name
    athlete_level (ChineseLevel): Athlete's pole sport level according to
      the Chinese methodology.
    date_joined (datetime | None): Date the athlete started being a client.
  """

  id: int
  user_id: int | None
  trainer_id: int | None
  name: PersonName | None
  athlete_level: ChineseLevel | None
  date_joined: datetime | None


@dataclass
class PersistedTrainer:
  """
  Represents an trainer fetched from a repository.

  Attributes:
    id (int): Internal unique identifyer of the trainer.
    user_id (int): Internal unique identifyer of the trainer's user.
    full_name(PersonName | None): Trainer's full name
    trainer_level (ChineseLevel): Trainer's pole sport level  certification
      according to the Chinese methodology.
  """

  id: int
  user_id: int | None
  name: PersonName | None
  trainer_level: ChineseLevel | None
  date_joined: datetime | None


@dataclass
class AthleteQueryFilter:
  athlete_ids: Collection[int] | None
  trainer_ids: Collection[int] | None
  athlete_levels: Collection[ChineseLevel] | None
  joined_between: DateRange | None


@dataclass
class TrainerQueryFilter:
  trainer_ids: Collection[int] | None
  trainer_levels: Collection[ChineseLevel] | None
  joined_between: DateRange | None
