# what you'l find here : logical services for the authentication layer
# how to deal with this file : each function is it's own block, no continuity

def hash_password(plain_text_password):
    # hash the password
    # return the hash as a string, to be stored in the database
    return

def verify_password(plain_text_password, stored_hash):
    # compare the plain text password against after hashing it (using the same hash) the stored hash
    # return True if they match, False otherwise
    return

def start_session(user_id):
    # after what i read so far, it seems python uses a token system
    # am still reading, you do it if you want, you can change the name to be more descriptive
    return

def register_user(username, email, password):
    # check if a user with this email already exists via get_user_by_email()
    # if they do, raise an error
    # hash the password
    # call create_user() with the hashed password
    # return the new user's id
    return

def login_user(email, password):
    # fetch the user by email via get_user_by_email()
    # if no user found, raise an error
    # verify the password against the stored hash
    # if wrong, raise an error
    # handle session or whatever using that token shit 
    return