from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import BinaryExpression, select
from sqlalchemy.orm import Session, joinedload

from ..domain.entities import (
  AthleteQueryFilter,
  PersistedAthlete,
  PersistedTrainer,
  PersonName,
  TrainerQueryFilter,
  UserAccess,
  VolatileAthlete,
  VolatileTrainer,
)
from ..domain.entities import ChineseLevel as Level
from ..domain.ports import UserRoleRepository
from .models import Athlete, Trainer, User, UserInfo

# TODO check if asynchronous code is really asynchronous in every method.


@dataclass
class UserRepositorySQLalchemy(UserRoleRepository):
  session: Session

  # TODO first we need to decide about how to authenticate users.
  # async def persist_user(self, user: VolatileUser) -> None:
  #   pass

  async def persist_athlete(self, new_athlete: VolatileAthlete) -> None:
    user_info = UserInfo()
    user_info.first_name = new_athlete.full_name.first_name
    user_info.second_name = new_athlete.full_name.second_name

    user = User()
    user.access_type = UserAccess.ATHLETE

    athlete = Athlete()
    athlete.user = user
    athlete.trainer_id = VolatileAthlete.trainer_id
    athlete.chinese_level = new_athlete.athlete_level

    self.session.add(user)
    self.session.add(athlete)
    self.session.commit()

  async def persist_trainer(self, new_trainer: VolatileTrainer) -> None:
    user_info = UserInfo()
    user_info.first_name = new_trainer.full_name.first_name
    user_info.second_name = new_trainer.full_name.second_name

    user = User()
    user.access_type = UserAccess.TRAINER
    user.user_info = user_info

    trainer = Trainer()
    trainer.chinese_level = new_trainer.trainer_level
    trainer.user = user

    self.session.add(user)
    self.session.add(trainer)
    self.session.commit()

  # TODO first we need to decide about how to authenticate users.
  # @abstractmethod
  # async def fetch_user():
  #   pass

  async def fetch_athletes(
    self, filters: AthleteQueryFilter
  ) -> tuple[PersistedAthlete, ...]:
    filter_clauses: list[BinaryExpression[bool]] = []
    if filters.athlete_ids is not None:
      filter_clauses.append(Athlete.id.in_(filters.athlete_ids))
    if filters.trainer_ids is not None:
      filter_clauses.append(Athlete.id.in_(filters.trainer_ids))
    if filters.athlete_levels is not None:
      filter_clauses.append(Athlete.id.in_(filters.athlete_levels))
    if filters.joined_between is not None:
      filter_clauses.append(
        Athlete.date_joined.between(
          filters.joined_between.start, filters.joined_between.finish
        )
      )

    athletes: Sequence[Athlete] = self.session.scalars(
      select(Athlete)
      .options(
        joinedload(Athlete.user).joinedload(User.user_info),
        joinedload(Athlete.chinese_level),
      )
      .where(*filter_clauses)
    ).all()

    return tuple(
      map(
        lambda db_athlete: PersistedAthlete(
          id=db_athlete.id,
          user_id=db_athlete.user_id,
          trainer_id=db_athlete.trainer_id,
          name=PersonName(
            db_athlete.user.user_info.first_name,
            db_athlete.user.user_info.second_name,
          ),
          athlete_level=Level(db_athlete.chinese_level.name),
          date_joined=db_athlete.date_joined,
        ),
        athletes,
      )
    )

  async def fetch_trainers(
    self, filters: TrainerQueryFilter
  ) -> tuple[PersistedTrainer, ...]:
    filter_clauses: list[BinaryExpression[bool]] = []
    if filters.trainer_ids is not None:
      filter_clauses.append(Trainer.id.in_(filters.trainer_ids))
    if filters.trainer_levels is not None:
      filter_clauses.append(Trainer.id.in_(filters.trainer_levels))
    if filters.joined_between is not None:
      filter_clauses.append(
        Trainer.date_joined.between(
          filters.joined_between.start, filters.joined_between.finish
        )
      )

    trainers = self.session.scalars(
      select(Trainer)
      .options(
        joinedload(Trainer.user).joinedload(User.user_info),
        joinedload(Trainer.chinese_level),
      )
      .where(*filter_clauses)
    ).all()

    return tuple(
      map(
        lambda db_trainer: PersistedTrainer(
          id=db_trainer.id,
          user_id=db_trainer.user_id,
          name=PersonName(
            db_trainer.user.user_info.first_name,
            db_trainer.user.user_info.second_name,
          ),
          trainer_level=Level(db_trainer.chinese_level.name),
          date_joined=db_trainer.date_joined,
        ),
        trainers,
      )
    )

  async def get_trainer_id(self, user_id: int) -> int | None:
    return self.session.scalar(
      select(User.trainer_id).where(User.id == user_id)
    )

  async def get_athlete_id(self, user_id: int) -> int | None:
    return self.session.scalar(
      select(User.athlete_id).where(User.id == user_id)
    )

  async def fetch_trainers_athletes_ids(self, trainer_id: int) -> set[int]:
    return set(
      self.session.scalars(
        select(Athlete.id).where(Athlete.trainer_id == trainer_id)
      )
    )
