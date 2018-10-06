from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
#from security import authenticate, identify
from db import db
from resources.cat import Cat, ListCats, ListAdoptedCats
from resources.user import User, ListUsers

app = Flask(__name__)
app.secret_key = 'MY_SECRET_KEY :p'   # a secret key must be specified
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"


api = Api(app)
#jwt = JWT(app, authenticate, identify)

api.add_resource(ListCats, '/cats')
api.add_resource(ListAdoptedCats, '/cats/adopted')
api.add_resource(Cat, '/cat/<string:catname>')
api.add_resource(ListUsers, '/users')
api.add_resource(User, '/user/<string:name>')


@app.before_first_request # execute the following function before the first request
def create_tables():
    db.create_all()


db.init_app(app)
app.run(port=5000,debug=True)
