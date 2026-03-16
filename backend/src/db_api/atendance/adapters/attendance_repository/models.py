from datetime import datetime

from sqlalchemy import (
  DateTime,
  ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_api.shared_kernel.adapters.models import Athlete, Base, IdMixin, Trainer


class Attendance(IdMixin, Base):
  __tablename__ = "atendances"

  athelte_id: Mapped[int] = mapped_column(ForeignKey("athletes.id"))
  trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.id"))
  support_trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.id"))
  date: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), nullable=False
  )

  athlete: Mapped[Athlete] = relationship(back_populates="attendances")
  trainer: Mapped[Trainer] = relationship(foreign_keys=[trainer_id])
  support_trainer: Mapped[Trainer] = relationship(
    foreign_keys=[support_trainer_id]
  )
