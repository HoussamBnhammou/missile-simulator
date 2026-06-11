#note : still learning flask, i'll write pseudo code, translation to be done later 

# POST /groups/<group_id>/expenses
    # extract data from request body
    # validate all required fields are present, return error if not
    # get user_id from the session, this is the paid_by value
    # call expense_service.create_expense()
    # return sucess with the new expense's id

# GET /groups/<group_id>/expenses
    # call expense_service.get_expenses_for_group()
    # return sucess with the list of expenses

# GET /expenses/<expense_id>
    # call expense_service.get_expense()
    # return sucess with the expense and its splits

# PATCH /expenses/<expense_id>
    # extract data from request body (all optional)
    # call expense_service.update_expense()
    # return sucess with success confirmation

# DELETE /expenses/<expense_id>
    # call expense_service.delete_expense()
    # return sucess with success confirmation

# GET /groups/<group_id>/balances
    # call expense_service.calculate_balances()
    # return sucess with the list of { from_user, to_user, amount_cents }

# PATCH /expenses/<expense_id>/splits/<user_id>
    # extract settled from request body, validate it is True
    # call expense_service.settle_debt()
    # return sucess with success confirmation