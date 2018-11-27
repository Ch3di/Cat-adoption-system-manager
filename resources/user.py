from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, jwt_required
from models.user import UserModel
from models.cat import CatModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstName', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('lastName', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('address', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    @jwt_required
    def get(self,username):
        user_json = get_jwt_identity()
        user = UserModel.findUserByUsername(user_json['username'])
        if user:
            return user.json()
        return { 'message': 'user not found'}, 404

    def post(self,username):
        user = UserModel.findUserByUsername(username)
        if user:
            return { 'message': 'the user has already existed'}, 400
        data = User.parser.parse_args()
        data['password'] = UserModel.generateHash(data['password'])
        user = UserModel(username, **data)
        user.saveToDB()
        return user.json()

    #improve put method
    def put(self, username):
        data = User.parser.parse_args()
        user = UserModel.findUserByUsername(username)
        if user:
            user.firstName = data['firstName']
            user.lastName = data['lastName']
            user.address = data['address']
            user.password = UserModel.generateHash(data['password'])
        else:
            data['password'] = UserModel.generateHash(data['password'])
            user = UserModel(username, **data)
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
        return { 'message': 'permission is not permitted. You need admin priviliges to delete a user'}, 400

class ListUsers(Resource):
    def get(self):
        return { 'users': [ { user.username : user.json() } for user in UserModel.query.all()] }

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

class SuperUser(Resource):
    @jwt_required
    def post(self, username):
        user_json = get_jwt_identity()
        if user_json['admin'] == False:
            return { "message": "You must be a super user to grant priviliges to other users" }, 400
        user = UserModel.findUserByUsername(username)
        if user:
            user.makeUserAdmin()
            return { "message" : "{} is now an admin".format(user.username) }, 200
        return { "message": "The requested user does not existed" }

class AdoptCat(Resource):
    @jwt_required
    def post(self, catname):
        user_json = get_jwt_identity()
        cat = CatModel.findCatsByCatname(catname)
        if cat and cat.adopter_id is None:
            cat.adopter_id = user_json['user-id']
            cat.adopted = True
            cat.saveToDB()
            return { 'message': 'congratulation ! Thank you for adopting {}'.format(catname) }, 200
        elif cat and cat.adopter_id is not None:
            return { 'message': 'This cat has already adopted ! Thanks anyway'}, 400
        else:
            return { 'message': 'could not find the requested cat' }, 404
