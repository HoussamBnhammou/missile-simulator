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
    # query all expenses for the given group_id where deleted_at IS NULL
    # return a list of expense dictionaries
    return

def update_expense(expense_id, data):
    # update whatever data columns we decide on for the given expense_id
    return

def delete_expense(expense_id):
    # set deleted_at = now on the expenses row for the given expense_id
    # DO NOT DELETE THE ROW
    return 