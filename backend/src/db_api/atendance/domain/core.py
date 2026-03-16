from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Sequence

from db_api.shared_kernel.domain.entities import UserAccess
from db_api.shared_kernel.domain.exceptions import (
  ForbidenResourceError,
  MissingAthleteIdError,
  MissingTrainerIdError,
)
from db_api.shared_kernel.domain.ports import UserRoleRepository

from .entities import (
  AttendanceQuery,
  AttendanceRecord,
  AuthenticatedUser,
  VolatileAttendanceRecord,
)
from .outbound import AttendanceRepository

# NOTE the async functions technically incur in a violation of the principle of
# isolation of the domain of the hexagonal architecture. This is because those
# method wouldn't be async if the repositories they use were using did not use
# I/O bound operations, in fewer words, those methods depend on the
# implementation of the ports. This violation is small enough for me to ignore,
# specialy since we plan to to use external databases anyway.
#
# For reasons like this the ports are technically part of the application layer
# although in many implementations of the hexagonal architecture this detail is
# ignored, which is understandable since the level of dependency is farly low
# and aside from some small and predictable details, the logic remains isolated.


@dataclass
class AttendanceCore:
  attdce_repository: AttendanceRepository
  user_repository: UserRoleRepository

  async def request_attendances(
    self, attendance_query: AttendanceQuery
  ) -> Sequence[AttendanceRecord]:
    result: Sequence[
      AttendanceRecord
    ] = await self.attdce_repository.fetch_attendances(attendance_query.filters)
    await self.validate_result(attendance_query.user, result)

    return result

  async def post_attendance(self, attendance: VolatileAttendanceRecord) -> None:
    await self.attdce_repository.persist_attendance(attendance)

  async def validate_result(
    self,
    user: AuthenticatedUser,
    attendances: Sequence[AttendanceRecord],
  ) -> None:
    """
    Validates if the passed user is allowed to get all of the requested
    attendances.
    """
    athletes_requested_ids = {
      attendance.athelte_id for attendance in attendances
    }
    match user.access:
      case UserAccess.TRAINER:
        trainer_id = await self.user_repository.get_trainer_id(user.id)
        if trainer_id is None:
          raise MissingTrainerIdError(user.id)
        trainer_athletes = (
          await self.user_repository.fetch_trainers_athletes_ids(trainer_id)
        )
        if not trainer_athletes >= athletes_requested_ids:
          not_assigned_athletes = athletes_requested_ids - trainer_athletes
          raise ForbidenResourceError(trainer_id, not_assigned_athletes)
      case UserAccess.ATHLETE:
        athlete_id = await self.user_repository.get_athlete_id(user.id)
        if athlete_id is None:
          raise MissingAthleteIdError(user.id)
        if athletes_requested_ids - {athlete_id} != set():
          raise ForbidenResourceError(
            athlete_id,
            athletes_requested_ids - {athlete_id},
          )
      case UserAccess.ADMIN:
        # If the access level is admin no checks are done.
        pass

  def get_past_month_date_range(self) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    first_day_this_month = now.replace(
      day=1, hour=0, minute=0, second=0, microsecond=0
    )
    last_day_last_month = first_day_this_month - timedelta(microseconds=1)
    first_day_last_month = last_day_last_month.replace(
      day=1, hour=0, minute=0, second=0, microsecond=0
    )
    return (first_day_last_month, last_day_last_month)

  def get_current_month_to_now(self) -> tuple[datetime, datetime]:
    """
    Gets the time interval from the start of the current month to now.

    Returns:
      tuple: A pair containing (start, end) timestamps.
        - start (datetime): The beginning of the interval.
        - end (datetime): The conclusion of the interval.

    """

    now = datetime.now(timezone.utc)
    first_day_this_month = now.replace(
      day=1, hour=0, minute=0, second=0, microsecond=0
    )
    return (first_day_this_month, now)
