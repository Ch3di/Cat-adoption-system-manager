from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

from models.user import UserModel



class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstName', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('lastName', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('address', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    def get(self,username):
        user = UserModel.findUserByUsername(username)
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

    def delete(self, username):
        user = UserModel.findUserByUsername(username)
        if user:
            user.deleteFromDB()
            return { 'message': 'user deleted' }, 202
        return { 'message': 'the requested user is not found' }, 404

class ListUsers(Resource):
    def get(self):
        return { 'users': [user.json() for user in UserModel.query.all()] }
