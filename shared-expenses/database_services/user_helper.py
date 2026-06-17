from database import db
from database_services.models import AppUser


# what you'll find here : database helpers for the users table
# how to deal with this file : each function is its own block, no continuity

################ FLAG ###############
# check the todos 


def get_user_by_email(email):
    # query the users table for a single row where email = email
    # used during login to find the user before verifying their password
    # return the row as a dictionary, or None if not found

    user = (
        db.session.query(AppUser)
        .filter(AppUser.email == email) # TODO: need to handle case sensivity 
        .first()
    )

    if user is None:
        return None

    return {
        "id": int(user.id),
        "username": user.username,
        "email": user.email,
        "password_hash": user.password_hash,
        "created_at": user.created_at.isoformat()
        if user.created_at
        else None,
    } # TODO : maybe a function that does this since it is recurrent 


def get_user_by_id(user_id):
    # query the users table for a single row where id = user_id
    # return the row as a dictionary, or None if not found

    user = (
        db.session.query(AppUser)
        .filter(AppUser.id == user_id)
        .first()
    )

    if user is None:
        return None

    return {
        "id": int(user.id),
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat()
        if user.created_at
        else None,
    }


def create_user(data):
    # insert a new row into the users table
    # return the newly created user's id

    username = data.get("username")
    email = data.get("email")
    password_hash = data.get("password_hash")

    if not username:
        raise ValueError("username is required")

    if not email:
        raise ValueError("email is required")

    if not password_hash:
        raise ValueError("password_hash is required")

    existing_user = (
        db.session.query(AppUser)
        .filter(AppUser.email == email) # TODO: need to handle case sensivity 
        .first()
    )

    if existing_user is not None:
        raise ValueError("email already exists")
    ## comment_houssam: Regarding the case sensitivity issue, i suggest we start by adding the email after making it all lower case.
    ## the comparison will be unified then by making sure to do a lower case tranforamtion before any comparison.
    user = AppUser(
        username=username,
        email=email,
        password_hash=password_hash,
    )

    db.session.add(user)
    db.session.commit()

    return int(user.id)