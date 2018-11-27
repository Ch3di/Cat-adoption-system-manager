from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_jwt_extended import JWTManager
from resources.cat import Cat, ListCats, ListAdoptedCats, IsAdopted, TakenCatname
from resources.user import User, ListUsers, UserLogin, TokenRefresh, SuperUser, AdoptCat, TakenUsername
from models.user import UserModel
import os

app = Flask(__name__)
app.secret_key = 'MY_SECRET_KEY :p'   # a secret key must be specified
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///data.db") # read the DATABASE_URL environment variable given by Heroku
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
api.add_resource(AdoptCat, '/adopt/<string:catname>')
api.add_resource(IsAdopted, '/isadopted/<string:catname>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(TakenCatname, '/cat/taken/<string:catname>')
api.add_resource(TakenUsername, '/user/taken/<string:username>')



if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)
