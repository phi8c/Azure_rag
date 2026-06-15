from sqlalchemy import (
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.core.database import Base


class Entity(Base):

    __tablename__ = "entities"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )