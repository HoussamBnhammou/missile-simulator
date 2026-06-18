from database import db, SCHEMA_NAME
from sqlalchemy import  UniqueConstraint, Identity, func


class AppUser(db.Model):
    __tablename__ = "APP_USERS"
    __table_args__ = (
        UniqueConstraint("USERNAME", name="UQ_APP_USERS_USERNAME"),
        UniqueConstraint("EMAIL", name="UQ_APP_USERS_EMAIL"),
        {"schema": SCHEMA_NAME},
    )

    id = db.Column(
        "ID",
        db.Numeric(38, 0),
        Identity(),
        primary_key=True,
    )

    username = db.Column(
        "USERNAME",
        db.String(255),
        nullable=False,
    )

    email = db.Column(
        "EMAIL",
        db.String(255),
        nullable=False,
    )

    password_hash = db.Column(
        "PASSWORD_HASH",
        db.String(255),
        nullable=False,
    )

    created_at = db.Column(
        "CREATED_AT",
        db.DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

    memberships = db.relationship(
        "Membership",
        back_populates="user",
        cascade="all, delete-orphan",
    )
