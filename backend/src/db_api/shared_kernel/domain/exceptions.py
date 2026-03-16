from typing import Collection


class DomainLayerError(Exception):
  """Base class for domain-level errors."""


class NotTrainerAthletesError(DomainLayerError):
  """
  Exception for when a trainer requests info about an athlete that is not
  assigned to them.
  """

  def __init__(self, trainer_id: int, athletes_ids: Collection[int]) -> None:
    self.trainer_id = trainer_id
    self.athletes_ids = athletes_ids
    super().__init__(
      f"Trainer with id: {trainer_id} has not been assigned to "
      f"athletes with ids: {list(athletes_ids)}"
    )


class NotAthletesInfoError(DomainLayerError):
  def __init__(self, user_id: int, athletes_ids: Collection) -> None:
    self.user_id = user_id
    self.athletes_ids = athletes_ids
    super().__init__(
      f"User with id: {user_id} does not have permission to access info"
      f"from users with ids: {list(athletes_ids)}."
    )


class ForbidenResourceError(DomainLayerError):
  pass


class MissingAthleteIdError(DomainLayerError):
  "Error for when a athlete does not have an id on the database."

  def __init__(self, user_id: int) -> None:
    super().__init__(
      f"User with id: {user_id} does not have an Athlete id on database"
    )


class MissingTrainerIdError(DomainLayerError):
  "Error for when a trainer does not have an id on the database."

  def __init__(self, user_id: int) -> None:
    super().__init__(
      f"User with id: {user_id} does not have a Trainer id on database"
    )
