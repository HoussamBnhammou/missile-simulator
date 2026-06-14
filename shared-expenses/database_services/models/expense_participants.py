from database import db, SCHEMA_NAME
from sqlalchemy import CheckConstraint, Identity, UniqueConstraint


class ExpenseParticipant(db.Model):
    __tablename__ = "EXPENSE_PARTICIPANTS"
    __table_args__ = (
        UniqueConstraint(
            "MEMBERSHIP_ID",
            "EXPENSE_ID",
            name="UQ_EXPENSE_PARTICIPANTS_MEMBER_EXPENSE",
        ),
        CheckConstraint(
            "SHARED_EXPENSE >= 0",
            name="CHK_SHARED_EXPENSE_POSITIVE",
        ),
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
            name="FK_EXPENSE_PARTICIPANTS_MEMBERSHIP",
        ),
        nullable=False,
    )

    expense_id = db.Column(
        "EXPENSE_ID",
        db.Numeric(38, 0),
        db.ForeignKey(
            f"{SCHEMA_NAME}.EXPENSES.ID",
            name="FK_EXPENSE_PARTICIPANTS_EXPENSE",
        ),
        nullable=False,
    )

    shared_expense = db.Column(
        "SHARED_EXPENSE",
        db.Numeric(10, 2),
        nullable=False,
    )

    membership = db.relationship(
        "Membership",
        back_populates="expense_participants",
    )

    expense = db.relationship(
        "Expense",
        back_populates="participants",
    )

    splits = db.relationship(
        "ExpenseSplit",
        back_populates="participant",
        cascade="all, delete-orphan",
    )
