from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

from models.cat import CatModel

class Cat(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('img_url', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('adopted', type=bool, required=True, help="This field cannot be left blank")
    parser.add_argument('sex', type=str, required=True, help="This field cannot be left blank")

# get, post, delete must be reviewed to check the identity of the user
    def get(self,catname):
        cat = CatModel.findCatsByCatname(catname)
        if cat:
            return cat.json()
        return { 'message': 'cat not found'}, 404

    def post(self,catname):
        if CatModel.findCatsByCatname(catname):
            return { 'message': 'This cat has already existed'}, 400
        data = Cat.parser.parse_args()
        cat = CatModel(catname,**data)
        cat.saveToDB()
        return cat.json(),201

    def put(self,catname):
        data = Cat.parser.parse_args()
        cat = CatModel.findCatsByCatname(catname)
        if cat:
            cat.name=data['name']
            cat.img_url=data['img_url']
            cat.adopted=data['adopted']
            cat.sex = data['sex']
        else:
            cat = CatModel(catname,**data)
        cat.saveToDB()
        return cat.json()

    def delete(self,catname):
        cat = CatModel.findCatsByCatname(catname)
        if cat:
            cat.deleteFromDB()
            return { 'message': 'cat was deleted successfully' }
        return { 'message': 'cat not found' }, 202

class ListCats(Resource):
    def get(self):
        return { 'cats': [cat.json() for cat in CatModel.query.all()]}

class ListAdoptedCats(Resource):
    def get(self):
        return { 'adopted-cats': [cat.json() for cat in CatModel.query.all()] }
