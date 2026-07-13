# what you'l find here : it's pretty obvious, it's one function
# how to deal with this file : --
from database import db
from database_services.models import ExpenseActivityLog

def write_log(expense_id, activity_type, old_value, membership_id, member_name, expense_name):
    # insert a new row into the activity_log table
    # data to be decided after seeing the database, might change over time 
    # this function is called by services before every mutation
    # data is defined as dict; {"expense_id":    , activity_type: add,edit or delete, old_value: XX (if vaiable), membership_id: who made the activity, member_name: username of the user }
    if expense_id is None:
        raise ValueError("expense_id is required")
    if activity_type is None:
        raise ValueError("activity_type is required")
    if old_value is None:
        raise ValueError("old_value is require")
    if membership_id is None:
        raise ValueError("member_id is required")
    


    activity = ExpenseActivityLog(
        expense_id = expense_id,
        activity_type = activity_type,
        old_value = old_value,
        membership_id = membership_id,
        message = member_name + " has " + activity_type  + "ed  expense " + expense_id
        )
    
    db.session.add(activity)
    db.session.commit()
    return int(activity.id)
