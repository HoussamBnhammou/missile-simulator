from decimal import Decimal, InvalidOperation
from database import db
from database_services.models import AppUser, Expense, ExpenseGroup, Membership
from datetime import datetime, timezone



# what you'l find here : database helpers for the users table
# how to deal with this file : each function is it's own block, no continuity

def create_expense(data):
    # insert a new row into the expenses table
    # return the newly created expense's id
    membership_id = data.get("membership_id")
    amount = data.get("expense")

    if membership_id is None:
        raise ValueError("membership_id is required")

    if amount is None:
        raise ValueError("expense is required")

    try:
        amount = Decimal(str(amount))
    except InvalidOperation:
        raise ValueError("expense must be a valid number")

    if amount <= 0:
        raise ValueError("expense must be greater than 0")

    expense = Expense(
        membership_id=membership_id,
        expense=amount,
    )

    db.session.add(expense)
    db.session.commit()

    return int(expense.id)
    


def get_expense_by_id(expense_id):
    # query the expenses table for a single row where id = expense_id
    # only return it if deleted_at IS NULL
    # return the row as a dictionary, or None if not found
    expense = (
        db.session.query(Expense)
        .join(Membership, Expense.membership_id == Membership.id)
        .join(ExpenseGroup, Membership.group_id == ExpenseGroup.id)
        .join(AppUser, Membership.user_id == AppUser.id)
        .filter(
            Expense.id == expense_id,
            Expense.deleted_at.is_(None),
        )
        .first()
    )
    if expense is None:
        return None
    

    return {
        "id": int(expense.id),
        "group_id": int(expense.membership.group_id),
        "membership_id": int(expense.membership_id),
        "paid_by": {
            "user_id": int(expense.membership.user.id),
            "username": expense.membership.user.username,
            "email": expense.membership.user.email,
        },
        "expense": float(expense.expense),
        "created_at": expense.created_at.isoformat()
        if expense.created_at
        else None,
        "deleted_at": expense.deleted_at.isoformat()
        if expense.deleted_at
        else None,
    }

def get_expenses_for_group(group_id):
    # query all expenses for the given group_id where deleted_at IS NULL
    # return a list of expense dictionaries
    expenses = (
        db.session.query(Expense)
        .join(Membership, Expense.membership_id == Membership.id)
        .join(ExpenseGroup, Membership.group_id == ExpenseGroup.id)
        .join(AppUser, Membership.user_id == AppUser.id)
        .filter(Membership.group_id == group_id)
        .filter(Expense.deleted_at.is_(None))
        .order_by(Expense.created_at.desc())
        .all()
    )

    result = []

    for expense in expenses:
        result.append(
            {
                "id": int(expense.id),
                "group_id": int(expense.membership.group_id),
                "membership_id": int(expense.membership_id),
                "paid_by": {
                    "user_id": int(expense.membership.user.id),
                    "username": expense.membership.user.username,
                    "email": expense.membership.user.email,
                },
                "expense": float(expense.expense),
                "created_at": expense.created_at.isoformat()
                if expense.created_at
                else None,
                "deleted_at": expense.deleted_at.isoformat()
                if expense.deleted_at
                else None,
            }
        )

    return result
    

def update_expense(expense_id, data):
    # update whatever data columns we decide on for the given expense_id
    return

def delete_expense(expense_id):
    # DO NOT DELETE THE ROW
    expense = (
        db.session.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.deleted_at.is_(None),
        )
        .first()
    )

    if expense is None:
        return None

    expense.deleted_at = datetime.now(timezone.utc)
    db.session.commit()

    return int(expense.id)