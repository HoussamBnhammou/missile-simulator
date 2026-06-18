from database import db
from database_services.models import AppUser, Membership
from datetime import datetime, timezone

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
    if group_id is None:
        raise ValueError("group_id is required")
    
    if user_id is None:
        raise ValueError("user_id is required")
    membership=(
    db.session.query(Membership)
    .filter(Membership.group_id == group_id)
    .filter(Membership.user_id == user_id)
    .first()
    )

    if membership is None:
        membership = Membership(
                        group_id=group_id,
                        user_id = user_id,
                    )
        db.session.add(membership)
        db.session.commit()

        return int(membership.id)

    else:
        membership.left_at = None
        db.session.commit()

        return int(membership.id)

def remove_member(group_id, user_id):
    # set left_at = now on the membership row for this group_id + user_id
    # DO NOT HARD DELETE THIS ROW !!!
    if group_id is None:
        raise ValueError("group_id is required")
    
    if user_id is None:
        raise ValueError("user_id is required")
    membership=(
    db.session.query(Membership)
    .filter(Membership.group_id == group_id)
    .filter(Membership.user_id == user_id)
    .first()
    )
    if membership is None:
        return None

    membership.left_at = datetime.now(timezone.utc)
    db.session.commit()

    return int(membership.id)

def get_members_for_group(group_id):
    # query memberships joined with users for the given group_id
    # only return rows where left_at IS NULL (meaning active members)
    # return a list of member dictionaries
    members_for_group = (
        db.session.query(Membership)
        .join(AppUser, Membership.user_id == AppUser.id)
        .filter(
            Membership.group_id == group_id,
            Membership.left_at.is_(None)
        )
    
    )

    result = []

    for member in members_for_group:
        result.append(
            {
                "id":int(member.id),
                "user_id":int(member.user_id),
                "group_id":int(member.group_id),
                "username":member.user.username
            }
        )

    return result

