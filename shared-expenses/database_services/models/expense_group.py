from database import db, SCHEMA_NAME
from sqlalchemy import  UniqueConstraint, Identity, func




class ExpenseGroup(db.Model):
    __tablename__ = "EXPENSE_GROUPS"
    __table_args__ = (
        {"schema": SCHEMA_NAME},
    )

    id = db.Column(
        "ID",
        db.Numeric(38, 0),
        Identity(),
        primary_key=True,
    )

    name = db.Column(
        "NAME",
        db.String(255),
        nullable=False,
    )
    
    deleted_at = db.Column(
        "DELETED_AT",
        db.DateTime,
        nullable=True,
    )

    memberships = db.relationship(
        "Membership",
        back_populates="group",
        cascade="all, delete-orphan",
    )