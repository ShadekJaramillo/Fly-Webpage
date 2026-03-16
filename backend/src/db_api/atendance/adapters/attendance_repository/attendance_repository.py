from dataclasses import asdict, dataclass
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from db_api.shared_kernel.domain.ports import UserRoleRepository

from ...domain.entities import (
  AttendanceQueryFilter,
  AttendanceRecord,
  VolatileAttendanceRecord,
)
from ...domain.outbound import AttendanceRepository
from .models import Attendance


@dataclass
class AttendanceRepositorySQLachemy(AttendanceRepository):
  session: Session
  user_repository: UserRoleRepository

  async def persist_attendance(
    self, new_attendance: VolatileAttendanceRecord
  ) -> None:
    self.session.add(Attendance(**asdict(new_attendance)))
    self.session.commit()

  async def fetch_attendances(
    self, filter: AttendanceQueryFilter
  ) -> Sequence[AttendanceRecord]:
    attendances: Sequence[Attendance] = self.session.scalars(
      select(Attendance)
      .where(
        Attendance.date.between(
          filter.date_range.start, filter.date_range.finish
        )
      )
      .where(Attendance.athelte_id.in_(filter.athlete_ids))
      .where(Attendance.trainer_id.in_(filter.trainer_ids))
      .where(Attendance.athelte_id.in_(filter.support_trainer_ids))
    ).all()

    return tuple(
      map(
        lambda mapped_attendance: AttendanceRecord(
          id=mapped_attendance.id,
          date=mapped_attendance.date,
          athelte_id=mapped_attendance.athelte_id,
          trainer_id=mapped_attendance.trainer_id,
          support_trainer_id=mapped_attendance.support_trainer_id,
        ),
        attendances,
      )
    )
