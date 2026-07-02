from database import db
from database_services.models import AppUser, Membership, ExpenseParticipant

# the database and models are confusing
# it give the impression that there 2 tables, one to track who participated and one for who owes what 
# but however you think about it, it's redundant and might lead to primary key conflicts
# at best it might force an extra level of complexity that is not really required  
# also looking the at the models it seems the split can't store more than one row

##participants should be a list of dicts that have membership_id and shared_expense: eg [{memebrship_id : "<value>", shared_expense: "<value>"},....

def create_participants(expense_id, participants):
    ##participants should be a list of dicts that have membership_id and shared_expense: eg [{memebrship_id : "<value>", shared_expense: "<value>"},....
    # insert one row into expense_participants for each participant
    # TO DO in the future : bulk insert if possible for efficiency
    ## To  bulk insert we should bypass the flask_sql_alchemy_library ORM layer and use sql_alchemy core, we don't need any optional extra complexity for now, we will leave for later.
    if expense_id == None:
        raise ValueError("expense_id is required")
    if participants == None or participants == []:
        raise ValueError("participants are required")

    
    expense_participant_ids = []

    for particpant in participants:

        expense_participant = ExpenseParticipant()
        expense_participant.expense_id = expense_id
        expense_participant.membership_id = particpant.membership_id
        expense_participant.shared_expense = particpant.shared_expense ## just realised the shared expense is the worst name i gave for this, it should be the opposite of shared.

        db.session.add(expense_participant)
        db.session.commit()
        expense_participant_ids.append(expense_participant.id)

    return expense_participant_ids

def get_participants_for_expense(expense_id):
    # query all rows in expense_participants where expense_id = expense_id
    # return a list of split dictionaries
    # important : should return enough information that we won't need other queries
    participants_for_expense = (db.session.query(ExpenseParticipant)
                          .join(Membership, ExpenseParticipant.membership_id == Membership.id)
                          .join(AppUser, Membership.user_id == AppUser.id)
                          .filter(ExpenseParticipant.expense_id == expense_id)
                         )
    
    results = []
    for participant in participants_for_expense:
        results.append(
            {
                "participant_id" : int(participant.id),
                "shared_expense" : float(participant.shared_expense),
                "group_id"       : int(participant.membership.group_id),
                "user_id"        : int(participant.membership.group_id),
                "username"       : participant.membership.user.username
            }
        )

    return results

def get_participants_for_group(group_id):
    # query all participants for all active expenses in the given group
    # used by the balances calculation 
    # return a list of split dictionaries
    # conceptually : must return who paid, who owes, how much
    return

def settle_split(expense_id, user_id):
    # i havn't seen setteled_at in any table in the schema
    # so can't really tell how it will be 
    # flag that the debt has been paid 
    ##comment_houssam: there will be no action of settling, the settling itself is the fact of paying the peeson you, then you just need to add an expense that includes the settled amount and that's it.
    return

def update_participants(expense_id, participants):
    # delete existing participants for this expense_id ?
    # re-insert with the new participants list
    # do smt to make sure it's atomic — either both happen or none of them happen 
    return

# deleting options are still dependant and the final schema design 