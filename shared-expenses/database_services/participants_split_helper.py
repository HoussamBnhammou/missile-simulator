# the database and models are confusing
# it give the impression that there 2 tables, one to track who participated and one for who owes what 
# but however you think about it, it's redundant and might lead to primary key conflicts
# at best it might force an extra level of complexity that is not really required  
# also looking the at the models it seems the split can't store more than one row


def create_splits(expense_id, participants):
    # participants is a list of ?
    # insert one row into expense_splits for each participant
    # bulk insert if possible for efficiency
    return

def get_splits_for_expense(expense_id):
    # query all rows in expense_splits where expense_id = expense_id
    # return a list of split dictionaries
    # important : should return enough information that we won't need other queries
    return

def get_splits_for_group(group_id):
    # query all splits for all active expenses in the given group
    # used by the balances calculation 
    # return a list of split dictionaries
    # conceptually : must return who paid, who owes, how much
    return

def settle_split(expense_id, user_id):
    # i havn't seen setteled_at in any table in the schema
    # so can't really tell how it will be 
    # flag that the debt has been paid 
    return

def update_splits(expense_id, participants):
    # delete existing splits for this expense_id ?
    # re-insert with the new participants list
    # do smt to make sure it's atomic — either both happen or none of them happen 
    return

# deleting options are still dependant and the final schema design 