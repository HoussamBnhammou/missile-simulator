#note : still learning flask, i'll write pseudo code, translation to be done later 

# POST /groups
    # extract name from request body
    # validate name is present, return error if not
    # get user_id from the session 
    # call group_service.create_group()
    # return sucess with the new group's id

# GET /groups
    # get user_id from the session
    # call group_service.get_groups_for_user()
    # return sucess with the list of groups

# GET /groups/<group_id>
    # call group_service.get_group()
    # return sucess with the group data

# PATCH /groups/<group_id>
    # extract name from request body
    # call group_service.update_group()
    # return sucess with success confirmation

# DELETE /groups/<group_id>
    # call group_service.delete_group()
    # return sucess with success confirmation

# POST /groups/<group_id>/members
    # extract user_id from request body
    # call group_service.add_member()
    # return sucess with success confirmation

# DELETE /groups/<group_id>/members/<user_id>
    # call group_service.remove_member()
    # return sucess with success confirmation