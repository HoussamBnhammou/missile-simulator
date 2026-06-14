from flask import jsonify
from database import db
from database_services.models import AppUser, Expense, ExpenseGroup, Membership



# what you'l find here : database helpers for the users table
# how to deal with this file : each function is it's own block, no continuity

def create_expense(data):
    # insert a new row into the expenses table
    # return the newly created expense's id
    return

def get_expense_by_id(expense_id):
    # query the expenses table for a single row where id = expense_id
    # only return it if deleted_at IS NULL
    # return the row as a dictionary, or None if not found
    return

def get_expenses_for_group(group_id):
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

    return jsonify(result), 200
    

def update_expense(expense_id, data):
    # update whatever data columns we decide on for the given expense_id
    return

def delete_expense(expense_id):
    # set deleted_at = now on the expenses row for the given expense_id
    # DO NOT DELETE THE ROW
    return 
