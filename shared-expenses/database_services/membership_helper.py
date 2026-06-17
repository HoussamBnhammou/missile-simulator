# what you'l find here : database helpers for the membership table
# how to deal with this file : each function is it's own block, no continuity

########### FLAG ############
# in adding a member we need to handle the case of rejoignin
# memeber joined, left, joined again 
# current pseudocode will simply add another row
# i can modify it for you if you want to implement this yourself 
# but ideally you investigate this since maybe it's a schema thing

def add_member(group_id, user_id):
    # insert a new row into memberships with group_id and user_id
    # set joined_at to current date, left_at to NULL
    return

def remove_member(group_id, user_id):
    # set left_at = now on the membership row for this group_id + user_id
    # DO NOT HARD DELETE THIS ROW !!!
    return

def get_members_for_group(group_id):
    # query memberships joined with users for the given group_id
    # only return rows where left_at IS NULL (meaning active members)
    # return a list of member dictionaries
    return