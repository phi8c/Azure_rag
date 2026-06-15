from sqlalchemy import (
    ForeignKey,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from pgvector.sqlalchemy import Vector

from app.core.database import Base


class EntityContext(Base):

    __tablename__ = "entity_contexts"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True
    )

    entity_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("entities.id"),
        nullable=False
    )

    chunk_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(1536),
        nullable=False
    )