import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Indicator(Base):
    __tablename__ = "indicators"

    indicator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.organization_id"),
        nullable=False,
    )

    finding_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("findings.finding_id"),
        nullable=True,
    )

    indicator_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
    )

    value: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    normalized_value: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        index=True,
    )

    source: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="email",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )