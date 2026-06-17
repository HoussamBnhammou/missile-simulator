from database import db
from database_services.models import ExpenseGroup, Membership


# what you'll find here : database helpers for the groups table
# how to deal with this file : each function is its own block, no continuity

def get_group_by_id(group_id):
    # query the groups table for a single row where id = group_id
    # return the row as a dictionary, or None if not found

    group = (
        db.session.query(ExpenseGroup)
        .filter(ExpenseGroup.id == group_id)
        .first()
    )

    if group is None:
        return None

    return {
        "id": int(group.id),
        "name": group.name,
    }


def get_groups_for_user(user_id):
    # query groups where the user has an active membership
    # active means membership.left_at IS NULL
    # return a list of group dictionaries

    groups = (
        db.session.query(ExpenseGroup)
        .join(Membership, Membership.group_id == ExpenseGroup.id)
        .filter(
            Membership.user_id == user_id,
            Membership.left_at.is_(None),
        )
        .all()
    )

    result = []

    for group in groups:
        result.append(
            {
                "id": int(group.id),
                "name": group.name,
            }
        )

    return result


def update_group_name(group_id, name):
    # update the name column on the groups table for the given group_id

    group = (
        db.session.query(ExpenseGroup)
        .filter(ExpenseGroup.id == group_id)
        .first()
    )

    if group is None:
        return None

    group.name = name
    db.session.commit()

    return int(group.id)


def create_group(data):
    # insert a new row into the groups table
    # return the newly created group's id

    name = data.get("name")

    if not name:
        raise ValueError("name is required")

    group = ExpenseGroup(
        name=name,
    )

    db.session.add(group)
    db.session.commit()

    return int(group.id)


def delete_group(group_id):
    ################ FLAG #################
    # we might need to handle if the group has any active expenses,
    # to be decided in testing (if it breaks smt)
    # if it does break smt, implement soft delete
    # if it doesn't, hard delete
    # for now let's just flag it
    ############### FLAG 2 ###############
    # even if this works it just means the delete order cascaded well
    # i feel soft delete is avoidable 
    # obv that has to be handled at the database first

    group = (
        db.session.query(ExpenseGroup)
        .filter(ExpenseGroup.id == group_id)
        .first()
    )

    if group is None:
        return None

    db.session.delete(group)
    db.session.commit()

    return int(group.id)