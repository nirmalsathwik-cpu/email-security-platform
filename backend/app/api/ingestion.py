from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.evidence_service import create_email_evidence


router = APIRouter(
    prefix="/ingestion",
    tags=["ingestion"],
)


class EmailIngestionRequest(BaseModel):
    organization_id: UUID
    user_id: UUID
    gmail_connection_id: UUID
    gmail_message_id: str
    received_at: datetime | None = None
    sender: str | None = None
    recipient: str | None = None
    subject: str | None = None


class EmailIngestionResponse(BaseModel):
    email_evidence_id: UUID
    gmail_message_id: str
    evidence_hash: str


@router.post(
    "/email",
    response_model=EmailIngestionResponse,
)
def ingest_email(
    request: EmailIngestionRequest,
    db: Session = Depends(get_db),
):
    email_data = {
        "received_at": request.received_at,
        "sender": request.sender,
        "recipient": request.recipient,
        "subject": request.subject,
    }

    evidence = create_email_evidence(
        db,
        organization_id=request.organization_id,
        user_id=request.user_id,
        gmail_connection_id=request.gmail_connection_id,
        gmail_message_id=request.gmail_message_id,
        email_data=email_data,
    )

    return EmailIngestionResponse(
        email_evidence_id=evidence.email_evidence_id,
        gmail_message_id=evidence.gmail_message_id,
        evidence_hash=evidence.evidence_hash,
    )