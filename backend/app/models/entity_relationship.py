from sqlalchemy import (
    ForeignKey,
    Float,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.core.database import Base


class EntityRelationship(Base):

    __tablename__ = "entity_relationships"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True
    )

    source_entity_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("entities.id"),
        nullable=False
    )

    target_entity_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("entities.id"),
        nullable=False
    )

    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0
    )