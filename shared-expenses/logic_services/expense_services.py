# what you'l find here : logical services for the expenses layer
# how to deal with this file : each function is it's own block, no continuity but they utilize each other

def validate_splits(amount, participants):
    # makesure the percentages and total amount to correct maths
    # i don't have the database details but this how i imagine :
    # sum up all share of each participant (after calc) across the participants list
    # if the sum does not equal total amount, raise a validation error
    # this must be called before creating or updating any expense
    return

def create_expense(data):
    # verify paid_by is an active member of the group
    # call validate_splits() to ensure the numbers add up
    # call create_expense() in expenses_helper to insert the expense
    # call whatever function we will have in participants_split_helper with the new expense's id
    # call write_log() in log_helper to record the creation
    # return the new expense's id
    return

def get_expenses_for_group(group_id, requesting_user_id):
    # verify the requesting user is an active member of the group
    # call get_expenses_for_group() in expenses_helper
    # return the list of expenses
    return

def get_expense(expense_id, requesting_user_id):
    # call get_expense_by_id() in expenses_helper
    # verify the requesting user is a member of the expense's group
    # return the expense with its splits attached
    return

def update_expense(data):
    # optional : verify the requesting user is the original paid_by if you want 
    # fetch the current expense state to use as the snapshot before modifying
    # call write_log() with the snapshot before making any changes (or verify)
    # call update_expense() in expenses_helper
    # changes to participants are particularly important, handle them
    # re-run validate_splits() if amounts changed
    return

def delete_expense(expense_id, requesting_user_id):
    # optinal : verify the requesting user is the original paid_by if you want 
    # fetch the current expense to use as the snapshot
    # call write_log() with the snapshot
    # call soft_delete_expense() in expenses_helper
    return

def calculate_balances(group_id, requesting_user_id):
    # verify the requesting user is an active member of the group
    # call get_splits_for_group() to get all unsettled splits
    # for each unsettled split, the user owes a share to the paid_by user
    # aggregate all debts between users
    # example: if A owes B 10 and B owes A 6, result is A owes B 4
    # return a list of { from_user, to_user, amount_cents }
    return

def settle_debt(expense_id, user_id, requesting_user_id):
    # verify the requesting user is the user_id being settled (can only settle your own debt)
    # call the database helper that marks a debt setteled
    # call write_log() to record the settlement
    return