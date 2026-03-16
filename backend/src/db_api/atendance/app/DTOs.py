from datetime import datetime, timezone
from enum import Enum
from typing import Self, Sequence
from uuid import UUID

from pydantic import BaseModel, model_validator

from db_api.shared_kernel.app.data_transfer_objects import Athlete


class PeriodPreset(Enum):
  LAST_MONTH = "last_month"
  CURRENT_MONTH = "current_month"
  NONE = None


class AttendanceFilterParams(BaseModel):
  athlete_ids: list[int]
  start: datetime
  finish: datetime


class AttendanceRequest(BaseModel):
  """
  Args:
    athlete_ids (set[int]): Set of ids of the athletes which attendances are
      being requested.
    trainer_ids (set[int]): Set of ids of the trainers which where present
      during the attendances.
    support_trainer_ids (set[int]): Set of ids of the trainers which athlete's
      attendances are being requested.
    period_preset (PeriodPreset): A period preset that can be specified for some
      common time periods. Can't be used if `start` or `finish` are passed.
    start (datetime): Start date of the interval from which the attendances are
      being requested. If passed, a value for `finish` must also be passed.
    finish (datetime): End date of the interval from which the attendances are
      being requested. If passed, a value for `start` must also be passed.
  """

  athlete_ids: set[int]
  trainer_ids: set[int]
  support_trainer_ids: set[int]
  period_preset: PeriodPreset | None = None
  start: datetime | None = None
  finish: datetime | None = None

  @model_validator(mode="after")
  def validate_logic_and_tz(self) -> Self:
    has_preset = self.period_preset is not None
    has_dates = self.start is not None and self.finish is not None

    # parameter exclusion check
    if has_preset and has_dates:
      raise ValueError(
        "Cannot provide both a period_preset and start/finish dates."
      )
    if not has_preset and not has_dates:
      raise ValueError(
        "Must provide either a period_preset or start/finish dates."
      )

    # preset validation
    if self.period_preset is not None:
      if self.period_preset not in PeriodPreset:
        raise ValueError(
          "Invalid preset, check documentation to see valid presets."
        )

    # date validations
    if self.start is not None and self.finish is not None:
      # timezone awareness chesck
      if (
        self.start.tzinfo is None
        or self.finish.tzinfo is None
        or self.start.tzinfo.utcoffset(None) is None
        or self.finish.tzinfo.utcoffset(None) is None
      ):
        failed: list[str] = []
        if (
          self.start.tzinfo is None or self.start.tzinfo.utcoffset(None) is None
        ):
          failed.append("start")

        if (
          self.finish.tzinfo is None
          or self.finish.tzinfo.utcoffset(None) is None
        ):
          failed.append("finish")

        if len(failed) > 1:
          message = "Arguments 'start' and 'finish' are not timezone aware"
        else:
          message = f"Argument {failed[0]} is not timezone aware"

        raise ValueError(message)

      # date order check
      if self.start > self.finish or self.finish > datetime.now(timezone.utc):
        raise ValueError("finish cannot be happening before start")

    return self


class Attendance(BaseModel):
  uuid: UUID
  date: datetime


class AttendanceResponse(BaseModel):
  athlete: Athlete
  attendances: Sequence[Attendance]
