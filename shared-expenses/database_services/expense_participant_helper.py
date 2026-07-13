from database import db
from database_services.models import AppUser, Membership, ExpenseParticipant, ExpenseGroup, Expense

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

    ###Flag####
        #this is the most heavy fetch we are doing on this app, i had to make sure we do it in an efficient way, for now complexity is query_time + nlog(n) where n is the returned rows of the query.
        # the query has 3 joints but it's the only way so i can do an efficient data manipulation after.
        # the results will be returned in the following format that exist in the end of the page __look__below__


    if group_id is None:
        raise ValueError("group_id is required")
    
    expenses_participants_per_group =   (
        db.session.query(Expense)
        .join(Membership, Expense.membership_id == Membership.id)
        .join(ExpenseGroup, Membership.group_id == ExpenseGroup.id)
        .join(ExpenseParticipant, Expense.id ==ExpenseParticipant.expense_id)
        .filter(Membership.group_id == group_id)
        .filter(Expense.deleted_at.is_(None))
        .order_by(Expense.created_at.desc())
        .all()
    )


    results = {}
    for expense_participants_per_group  in expenses_participants_per_group:
        if expense_participants_per_group.id in results:
            results[expense_participants_per_group.id].participants.append({ expense_participants_per_group.participants.membership_id :  expense_participants_per_group.participants.shared_expense })
        else:
            results[expense_participants_per_group.id] = {
                "payer" : expense_participants_per_group.paid_by,
                "price"      : expense_participants_per_group.expense,
                "participants": [{expense_participants_per_group.participants.membership_id :  expense_participants_per_group.participants.shared_expense}]
            }
    return results





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
    if expense_id is None:
        raise ValueError("expense_id is required")
    if participants is None or participants == []:
        raise ValueError("participants are required")
    participant_ids = []

    for participant in participants:
      
        participant_row = (
            db.session.query(ExpenseParticipant)
            .filter(ExpenseParticipant.membership_id == participant.membership_id)
            .filter(ExpenseParticipant.expense_id == expense_id )
            .first()
        )

        if participant_row is None:

            participant_row = ExpenseParticipant(
                membership_id =participant.membership_id ,
                expense_id = participant.expense_id ,
                shared_expense = participant.shared_expense    
            )
            db.session.add(participant_row)
            db.session.commit()


        else:
            participant_row.shared_expense = participant.shared_expense
            db.session.commit()

        participant_ids.append(participant_row.id)
    return participant_ids

# deleting options are still dependant and the final schema design 




## comment about the format of the result while fetching exepense participant per groups
# results = {
#     expense_id_1: {
#         "payer": payer_membership_id,
#         "price": expense_amount,
#         "participants": [
#             {
#                 participant_1_membership_id: participant_1_shared_expense,
#                 participant_2_membership_id: participant_2_shared_expense,
#                 # ...
#             }
#         ],
#     },
#     expense_id_2: {
#         "payer": payer_membership_id,
#         "price": expense_amount,
#         "participants": [
#             {
#                 participant_1_membership_id: participant_1_shared_expense,
#                 participant_2_membership_id: participant_2_shared_expense,
#                 # ...
#             }
#         ],
#     },
#     # ...
# }