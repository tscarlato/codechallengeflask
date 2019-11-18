from data import users


def login(email):
    # password is ignored
    return [user for user in users if email == user.get('email')][0]