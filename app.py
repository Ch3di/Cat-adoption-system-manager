from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_jwt_extended import JWTManager
from security import authenticate, identify
from db import db
from resources.cat import Cat, ListCats, ListAdoptedCats
from resources.user import User, ListUsers, UserLogin, SuperUser
from models.user import UserModel

app = Flask(__name__)
app.secret_key = 'MY_SECRET_KEY :p'   # a secret key must be specified
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

api = Api(app)
jwt = JWTManager(app)

api.add_resource(ListCats, '/cats')
api.add_resource(ListAdoptedCats, '/cats/adopted')
api.add_resource(Cat, '/cat/<string:catname>')
api.add_resource(ListUsers, '/users')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserLogin, '/login/<string:username>')
api.add_resource(SuperUser, '/user/grant/<string:username>')
@app.before_first_request # execute the following function before the first request
def create_tables():
    db.create_all()
    if UserModel.findUserByUsername('admin') is None:
        adminPassword = UserModel.generateHash('secretpass')
        admin = UserModel('admin','Admin','', '', adminPassword)
        admin.saveToDB()
        admin.makeUserAdmin()


db.init_app(app)
app.run(port=5000,debug=True)
