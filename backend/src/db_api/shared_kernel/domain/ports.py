from abc import ABC, abstractmethod

from .entities import (
  AthleteQueryFilter,
  PersistedAthlete,
  PersistedTrainer,
  TrainerQueryFilter,
  VolatileAthlete,
  VolatileTrainer,
)


class UserRoleRepository(ABC):
  @abstractmethod
  async def persist_athlete(self, athlete: VolatileAthlete):
    pass

  @abstractmethod
  async def persist_trainer(self, trainer: VolatileTrainer):
    pass

  # TODO first we need to decide about how to authenticate users.
  # @abstractmethod
  # async def fetch_user():
  #   pass

  @abstractmethod
  async def fetch_athletes(
    self, filter: AthleteQueryFilter
  ) -> PersistedAthlete:
    pass

  @abstractmethod
  async def fetch_trainers(
    self, filter: TrainerQueryFilter
  ) -> PersistedTrainer:
    pass

  @abstractmethod
  async def get_trainer_id(self, user_id: int) -> int | None:
    pass

  @abstractmethod
  async def get_athlete_id(self, user_id: int) -> int | None:
    pass

  @abstractmethod
  async def fetch_trainers_athletes_ids(self, trainer_id: int) -> set[int]:
    pass
