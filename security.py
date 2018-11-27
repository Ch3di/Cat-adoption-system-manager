from models.user import UserModel
from werkzeug.security import safe_str_cmp # compare strings safely


def authenticate(username, password):
    user = UserModel.findUserByUsername(username)
    if user and UserModel.verifyHash(password, user.password):
        return user

def identify(payload):
    id = payload['identity']
    return UserModel.findUserById(id)
