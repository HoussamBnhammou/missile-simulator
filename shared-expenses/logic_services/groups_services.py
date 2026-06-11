# what you'l find here : logical helpers for the groups layer
# how to deal with this file : each function is it's own block, no continuity

def create_group(name, created_by):
    # call create_group() in groups_helper
    # optinal : add the creator as the first member with role 'admin' (leave this as comment for later)
    # return the new group's id
    return

def get_groups_for_user(user_id):
    # call get_groups_for_user() in groups_helper
    # return the list of groups
    return

def get_group(group_id, requesting_user_id):
    # call get_group_by_id() in groups_helper
    # verify the requesting user is an active member of this group
    # if not, raise an error
    # return the group
    return

def update_group(group_id, name, requesting_user_id):
    # verify the requesting user is an creator of this group 
    # if not, raise error
    # call update_group_name() in groups_helper
    return

def delete_group(group_id, requesting_user_id):
    # verify the requesting user is the group creator (or maybe an admin system?)
    # call delete_group() in groups_helper
    return

def add_member(group_id, user_id, requesting_user_id):
    # verify the user being added exists
    # call add_member() in groups_helper
    return

def remove_member(group_id, user_id, requesting_user_id):
    # verify the requesting user is the group creator or is removing themselves
    # call remove_member() in groups_helper
    return