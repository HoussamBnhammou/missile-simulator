from database import db, SCHEMA_NAME
from sqlalchemy import CheckConstraint


class ExpenseSplit(db.Model):
    __tablename__ = "EXPENSE_SPLIT"
    __table_args__ = (
        CheckConstraint(
            "PERSONAL_EXPENSE >= 0",
            name="CHK_PERSONAL_EXPENSE_POSITIVE",
        ),
        {"schema": SCHEMA_NAME},
    )

    participant_id = db.Column(
        "PARTICIPANT_ID",
        db.Numeric(38, 0),
        db.ForeignKey(
            f"{SCHEMA_NAME}.EXPENSE_PARTICIPANTS.ID",
            name="FK_EXPENSE_SPLIT_PARTICIPANT",
        ),
        primary_key=True,
    )

    expense_id = db.Column(
        "EXPENSE_ID",
        db.Numeric(38, 0),
        db.ForeignKey(
            f"{SCHEMA_NAME}.EXPENSES.ID",
            name="FK_EXPENSE_SPLIT_EXPENSE",
        ),
        primary_key=True,
    )

    personal_expense = db.Column(
        "PERSONAL_EXPENSE",
        db.Numeric(10, 2),
        nullable=False,
    )

    participant = db.relationship(
        "ExpenseParticipant",
        back_populates="splits",
    )

    expense = db.relationship(
        "Expense",
        back_populates="splits",
    )
