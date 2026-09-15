import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class EmailEvidence(Base):
    __tablename__ = "email_evidence"

    email_evidence_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.organization_id"),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
    )

    gmail_connection_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("gmail_connections.gmail_connection_id"),
        nullable=False,
    )

    gmail_message_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    received_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    sender: Mapped[str | None] = mapped_column(
        String(320),
        nullable=True,
    )

    recipient: Mapped[str | None] = mapped_column(
        String(320),
        nullable=True,
    )

    subject: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    evidence_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    storage_reference: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )