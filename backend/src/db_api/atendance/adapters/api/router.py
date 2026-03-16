from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query

from ...app.DTOs import AttendanceRequest, AttendanceResponse
from ...domain.entities import AttendanceRecord
from ...domain.service import AttendanceService
from .dependencies import get_attendance_service

router = APIRouter(prefix="beta/attendances/", tags=["posts v0.1"])


@router.get("athlete/", response_model=list[AttendanceResponse])
async def get_attendances_endpoint(
  query: Annotated[AttendanceRequest, Query()],
  attendance_service: AttendanceService = Depends(get_attendance_service),  # noqa: B008
):
  try:
    result: Sequence[AttendanceRecord]

    match period_preset:
      case PeriodPreset.CURRENT_MONTH:
        result = await attendance_service.get_current_month(athlete_id)
      case PeriodPreset.LAST_MONTH:
        result = await attendance_service.get_last_month(athlete_id)
      case None:
        result = await attendance_service.get_between(athlete_id, start, finish)
      case _:
        raise HTTPException(status_code=400, detail="Invalid period preset")

    return result

  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/athlete/{athlete_id}/attendances")
def post_attendance_endpoint(
  athlete_id: int,
  payload: AttendanceRequest,
  service: AttendanceService = Depends(get_attendance_service),  # noqa: B008
):
  attendance = AttendanceRecord
  service.post_attendance()
