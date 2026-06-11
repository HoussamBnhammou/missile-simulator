# what you'l find here : database helpers for the groups table
# how to deal with this file : each function is it's own block, no continuity

def get_group_by_id(grou_id):
  # query the groups table for a single row where id = group_id
  # return the row as a dictionary, or None if not found
  return 

def get_groups_for_user(user_id):
  # query groups where the user has an active membership
  # active means membership.left_at IS NULL
  # return a list of group dictionaries
  return 

def update_group_name(group_id, name):
  # update the name column on the groups table for the given group_id
  return

def create_group(data):
  # insert a new row into the groups table
  # return the newly created group's id
  return 

def delete_group(group_id):
  ################ FLAG #################
  # we might need to handle if the group has any active expenses, to be decided in testing (if it breaks smt)
  # if it does break smt, implement soft delete
  # if it doesn't, hard delete
  # for now let's just flag it
  return 