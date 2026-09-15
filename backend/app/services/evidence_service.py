import hashlib
import json
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.email_evidence import EmailEvidence


def _json_safe(value: Any) -> Any:
    """Convert values into deterministic JSON-safe representations."""
    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, dict):
        return {
            str(key): _json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [_json_safe(item) for item in value]

    return value


def calculate_evidence_hash(email_data: dict[str, Any]) -> str:
    canonical_data = _json_safe(email_data)

    serialized = json.dumps(
        canonical_data,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(serialized).hexdigest()


def create_email_evidence(
    db: Session,
    *,
    organization_id,
    user_id,
    gmail_connection_id,
    gmail_message_id: str,
    email_data: dict[str, Any],
) -> EmailEvidence:
    existing = db.scalar(
        select(EmailEvidence).where(
            EmailEvidence.gmail_connection_id == gmail_connection_id,
            EmailEvidence.gmail_message_id == gmail_message_id,
        )
    )

    if existing is not None:
        return existing

    evidence = EmailEvidence(
        organization_id=organization_id,
        user_id=user_id,
        gmail_connection_id=gmail_connection_id,
        gmail_message_id=gmail_message_id,
        received_at=email_data.get("received_at"),
        sender=email_data.get("sender"),
        recipient=email_data.get("recipient"),
        subject=email_data.get("subject"),
        evidence_hash=calculate_evidence_hash(email_data),
        storage_reference=f"email-evidence/{gmail_message_id}",
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence