from hmac import compare_digest
from resources.user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user is not None and compare_digest(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
