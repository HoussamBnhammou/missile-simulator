
from database import db, SCHEMA_NAME
from sqlalchemy import  UniqueConstraint, Identity, func

class Membership(db.Model):
    __tablename__ = "MEMBERSHIP"
    __table_args__ = (
        UniqueConstraint("GROUP_ID", "USER_ID", name="UQ_MEMBERSHIP_GROUP_USER"),
        {"schema": SCHEMA_NAME},
    )

    id = db.Column(
        "ID",
        db.Numeric(38, 0),
        Identity(),
        primary_key=True,
    )

    group_id = db.Column(
        "GROUP_ID",
        db.Numeric(38, 0),
        db.ForeignKey(
            f"{SCHEMA_NAME}.EXPENSE_GROUPS.ID",
            name="FK_MEMBERSHIP_GROUP",
        ),
        nullable=False,
    )

    user_id = db.Column(
        "USER_ID",
        db.Numeric(38, 0),
        db.ForeignKey(
            f"{SCHEMA_NAME}.APP_USERS.ID",
            name="FK_MEMBERSHIP_USER",
        ),
        nullable=False,
    )

    joined_at = db.Column(
        "JOINED_AT",
        db.DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

    left_at = db.Column(
        "LEFT_AT",
        db.DateTime,
        nullable=True,
    )

    group = db.relationship(
        "ExpenseGroup",
        back_populates="memberships",
    )

    user = db.relationship(
        "AppUser",
        back_populates="memberships",
    )

    expenses = db.relationship(
        "Expense",
        back_populates="membership",
    )

    expense_participants = db.relationship(
        "ExpenseParticipant",
        back_populates="membership",
    )