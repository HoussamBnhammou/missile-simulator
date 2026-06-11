#note : still learning flask, i'll write pseudo code, translation to be done later 


# POST /auth/register
    # extract username, email, password from request body
    # validate that all three fields are present, return error if not
    # call auth_services.register_user()
    # return sucess (201?) with the new user's id

# POST /auth/login
    # extract email and password from request body
    # validate that both fields are present, return error if not
    # call auth_services.login_user()
    # return sucess with the flask session shit (tokens or whatever)