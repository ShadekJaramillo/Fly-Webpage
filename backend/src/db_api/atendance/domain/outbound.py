from abc import ABC, abstractmethod
from typing import Sequence

from .entities import (
  AttendanceQueryFilter,
  AttendanceRecord,
  VolatileAttendanceRecord,
)

"""
This module contains the ports that the interfaces that their respective
adapters must implement.

"""


class AttendanceRepository(ABC):
  @abstractmethod
  async def persist_attendance(
    self, new_attendance: VolatileAttendanceRecord
  ) -> None:
    pass

  @abstractmethod
  async def fetch_attendances(
    self, filter: AttendanceQueryFilter
  ) -> Sequence[AttendanceRecord]:
    pass
