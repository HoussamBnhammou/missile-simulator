from database import db, SCHEMA_NAME
from sqlalchemy import Identity, func


class ExpenseActivityLog(db.Model):
    __tablename__ = "EXPENSE_ACTIVITY_LOG"
    __table_args__ = (
        {"schema": SCHEMA_NAME},
    )

    id = db.Column(
        "ID",
        db.Numeric(38, 0),
        Identity(),
        primary_key=True,
    )

    expense_id = db.Column(
        "EXPENSE_ID",
        db.Numeric(38, 0),
        db.ForeignKey(
            f"{SCHEMA_NAME}.EXPENSES.ID",
            name="FK_EXPENSE_ACTIVITY_LOG_EXPENSE",
        ),
        nullable=False,
    )

    activity_type = db.Column(
        "ACTIVITY_TYPE",
        db.String(100),
        nullable=False,
    )

    message = db.Column(
        "MESSAGE",
        db.String(255),
        nullable=True,
    )
    
    created_at = db.Column(
        "CREATED_AT",
        db.DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )
    old_value = db.Column(
        "OLD_VALUE",
        db.Numeric(10, 2),
        nullable=True,
    )

    expense = db.relationship(
        "Expense",
        back_populates="activity_logs",
    )


