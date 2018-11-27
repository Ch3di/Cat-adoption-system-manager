from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, jwt_required
from models.user import UserModel
from models.cat import CatModel


class User(Resource):

    def get(self,username):
        user = UserModel.findUserByUsername(username)
        if user:
            return user.json()
        return { 'message': 'user not found'}, 404

    def post(self,username):
        parser = reqparse.RequestParser()
        parser.add_argument('first-name', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('last-name', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('address', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('email', type=str)
        parser.add_argument('phone', type=str)
        user = UserModel.findUserByUsername(username)
        if user:
            return { 'message': 'the user has already existed'}, 400
        data = parser.parse_args()
        data['password'] = UserModel.generateHash(data['password'])
        data['firstName'] = data['first-name']
        data['lastName'] = data['last-name']
        data.pop('first-name', None)
        data.pop('last-name', None)
        user = UserModel(username, **data)
        user.saveToDB()
        return user.json()

    @jwt_required
    def put(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('firstName', type=str)
        parser.add_argument('lastName', type=str)
        parser.add_argument('address', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('phone', type=str)
        data = parser.parse_args()
        user_json = get_jwt_identity()
        if user_json['username'] != username or user_json['admin']==False:
            return { 'message': "Not permitted action" }, 401
        user = UserModel.findUserByUsername(username)
        if data['firstName']:
            user.firstName = data['firstName']
        if data['lastName']:
            user.lastName = data['lastName']
        if data['address']:
            user.address = data['address']
        if data['password']:
            user.password = UserModel.generateHash(data['password'])
        if data['email']:
            user.email = data['email']
        if data['phone']:
            user.phone = data['phone']
        user.saveToDB()
        return user.json()

    # only admin can delete other users
    # the user can delete his account too
    @jwt_required
    def delete(self, username):
        admin_json = get_jwt_identity()
        if admin_json['admin'] == True or admin_json['username']== username:
            user = UserModel.findUserByUsername(username)
            if user:
                user.deleteFromDB()
                return { 'message': 'user deleted' }, 202
            return { 'message': 'the requested user is not found' }, 404
        return { 'message': 'permission is not permitted. You need admin privileges to delete a user'}, 400

class ListUsers(Resource):
    @jwt_required
    def get(self):
        user_json = get_jwt_identity()
        if user_json['admin'] == True:
            return { 'users': [ { user.username : user.json() } for user in UserModel.query.all()] }
        return { 'message': 'Permission denied'}, 401
class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help="You cannot login without a password")

    def post(self, username):
        data = UserLogin.parser.parse_args()
        user = UserModel.findUserByUsername(username)
        try:
            isCorrect = UserModel.verifyHash(data['password'], user.password)
        except:
            isCorrect = False
        if user and isCorrect:
            access_token = create_access_token(identity = user.json())
            refresh_token = create_refresh_token(identity = user.json())
            return {
                'message': 'Logged in as {}'.format(user.username),
                'access-token': access_token,
                'refresh-token': refresh_token
                }, 200
        return { 'message': "username or password is not correct" }, 400

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user_json = get_jwt_identity()
        access_token = create_access_token(identity = user_json)
        return {'access-token': access_token}

class SuperUser(Resource):
    @jwt_required
    def post(self, username):
        user_json = get_jwt_identity()
        if user_json['admin'] == False:
            return { "message": "You must be a super user to grant privileges to other users" }, 400
        user = UserModel.findUserByUsername(username)
        if user:
            user.makeUserAdmin()
            return { "message" : "{} is now an admin".format(user.username) }, 200
        return { "message": "The requested user does not existed" }, 404

class AdoptCat(Resource):
    @jwt_required
    def post(self, catname):
        user_json = get_jwt_identity()
        cat = CatModel.findCatsByCatname(catname)
        if cat and cat.adopter_id is None:
            cat.adopter_id = user_json['user-id']
            cat.adopted = True
            cat.saveToDB()
            return { 'message': 'congratulations ! Thank you for adopting {}'.format(cat.name) }, 200
        elif cat and cat.adopter_id is not None:
            return { 'message': 'This cat has already adopted ! Thanks anyway'}, 400
        else:
            return { 'message': 'could not find the requested cat' }, 404

class TakenUsername(Resource):
    def get(self, username):
        user = UserModel.findUserByUsername(username)
        if user:
            return { 'taken': True }, 400
        return {'taken': False}
