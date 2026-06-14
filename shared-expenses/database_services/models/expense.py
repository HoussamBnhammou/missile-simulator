
from database import db, SCHEMA_NAME
from sqlalchemy import  CheckConstraint, Identity, func


class Expense(db.Model):
    __tablename__ = "EXPENSES"
    __table_args__ = (
        CheckConstraint("EXPENSE > 0", name="CHK_EXPENSES_AMOUNT_POSITIVE"),
        {"schema": SCHEMA_NAME},
    )

    id = db.Column(
        "ID",
        db.Numeric(38, 0),
        Identity(),
        primary_key=True,
    )

    membership_id = db.Column(
        "MEMBERSHIP_ID",
        db.Numeric(38, 0),
        db.ForeignKey(
            f"{SCHEMA_NAME}.MEMBERSHIP.ID",
            name="FK_EXPENSES_MEMBERSHIP",
        ),
        nullable=False,
    )

    expense = db.Column(
        "EXPENSE",
        db.Numeric(10, 2),
        nullable=False,
    )

    created_at = db.Column(
        "CREATED_AT",
        db.DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

    deleted_at = db.Column(
        "DELETED_AT",
        db.DateTime,
        nullable=True,
    )

    membership = db.relationship(
        "Membership",
        back_populates="expenses",
    )

    participants = db.relationship(
        "ExpenseParticipant",
        back_populates="expense",
        cascade="all, delete-orphan",
    )

    splits = db.relationship(
        "ExpenseSplit",
        back_populates="expense",
        cascade="all, delete-orphan",
    )

    activity_logs = db.relationship(
        "ExpenseActivityLog",
        back_populates="expense",
        cascade="all, delete-orphan",
    )
