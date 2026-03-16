from functools import partial

from nanoid import generate
from sqlalchemy import (
  String,
)
from sqlalchemy.orm import Mapped, mapped_column

PUBLIC_ID_LENGTH = 12
generate_public_id = partial(generate, size=PUBLIC_ID_LENGTH)


class IdMixin:
  id: Mapped[int] = mapped_column(primary_key=True)
  public_id: Mapped[str] = mapped_column(
    String(12, collation="latin1_bin"),
    default=generate_public_id,
    unique=True,
    index=True,
    nullable=False,
  )
