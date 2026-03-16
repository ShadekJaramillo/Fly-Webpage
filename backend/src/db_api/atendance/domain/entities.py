from dataclasses import dataclass
from datetime import datetime

from db_api.shared_kernel.domain.entities import AuthenticatedUser, DateRange


@dataclass
class VolatileAttendanceRecord:
  """
  Record of an attendance of an athlete not persisted to a reposiroty yet.

  Args:
    date (datetime): date of the attendance.
    athlete_id (int): Internal unique identifyer of the athlete attending.
    trainer_id (int): Internal unique identifyer of the trainer directing
      the class.
    suport_trainer_id (int | None): Internal unique identifyer of the
      support trainer who assited the athlete during the class.
  """

  date: datetime
  athelte_id: int
  trainer_id: int
  support_trainer_id: int | None


@dataclass
class AttendanceRecord:
  """
  Record of an attendance of an athlete to a class fetched from a reposiroty.

  Args:
    id (int): Internal unique identifyer of the attendance record.
    date (datetime): date of the attendance.
    athlete_id (int): Internal unique identifyer of the athlete attending.
    trainer_id (int): Internal unique identifyer of the trainer directing
      the class.
    suport_trainer_id (int | None): Internal unique identifyer of the
      support trainer who assited the athlete during the class.
  """

  id: int
  date: datetime
  athelte_id: int
  trainer_id: int
  support_trainer_id: int | None


@dataclass
class AttendanceQueryFilter:
  """
  Filter object for attendance record queries.

  Args:
    date_range (DateRange): Object representing the date range of the
      attendances being queried.
    athlete_ids (set[int]): List of unique identifiers of the athletes
      whose attendances are being queried.
    trainer_ids (set[int]): List of unique identifiers of the trainers
      whose athletes attendances are being queried.
    support_trainer_ids (set[int]): List of unique identifiers of the
      support trainers whose athletes attendances are being queried.
  """

  date_range: DateRange
  athlete_ids: set[int]
  trainer_ids: set[int]
  support_trainer_ids: set[int]


@dataclass
class AttendanceQuery:
  """
  Query object for retrieving attendance records.

  Args:
    user (User): The user making the request.
    filters (AttendanceQueryFilter): Object with the details of how the
      query is being made.
  """

  user: AuthenticatedUser
  filters: AttendanceQueryFilter
