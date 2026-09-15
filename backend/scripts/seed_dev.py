import uuid

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.organization import Organization
from app.models.user import User
from app.models.gmail_connection import GmailConnection


def seed() -> None:
    db = SessionLocal()

    try:
        organization = db.scalar(
            select(Organization).where(
                Organization.name == "Development Organization"
            )
        )

        if organization is None:
            organization = Organization(
                name="Development Organization",
            )
            db.add(organization)
            db.flush()

        user = db.scalar(
            select(User).where(
                User.email_address == "dev@example.test"
            )
        )

        if user is None:
            user = User(
                organization_id=organization.organization_id,
                email_address="dev@example.test",
                display_name="Development User",
            )
            db.add(user)
            db.flush()

        connection = db.scalar(
            select(GmailConnection).where(
                GmailConnection.gmail_account_email == "dev@example.test"
            )
        )

        if connection is None:
            connection = GmailConnection(
                organization_id=organization.organization_id,
                user_id=user.user_id,
                gmail_account_email="dev@example.test",
            )
            db.add(connection)

        db.commit()

        print("Development seed complete")
        print(f"organization_id={organization.organization_id}")
        print(f"user_id={user.user_id}")
        print(f"gmail_connection_id={connection.gmail_connection_id}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()