from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.cat import CatModel

class Cat(Resource):
# get, post, delete must be reviewed to check the identity of the user
    def get(self,catname):
        cat = CatModel.findCatsByCatname(catname)
        if cat:
            return cat.json()
        return { 'message': 'cat not found'}, 404

    @jwt_required
    def post(self,catname):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('img_url', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('adopted', type=bool, required=True, help="This field cannot be left blank")
        parser.add_argument('sex', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('color', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('age-day', type=str)
        parser.add_argument('age-month', type=str)
        parser.add_argument('age-year', type=str)
        if CatModel.findCatsByCatname(catname):
            return { 'message': 'This catname has already taken'}, 400
        data = parser.parse_args()
        if data['age-day']:
            data['ageD'] = data['age-day']
        if data['age-month']:
            data['ageM'] = data['age-month']
        if data['age-year']:
            data['ageY'] = data['age-year']
        user_json = get_jwt_identity()
        cat = CatModel(catname, user_json['user-id'], **data)
        cat.saveToDB()
        return cat.json(), 201

    @jwt_required
    def put(self,catname):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('img_url', type=str)
        parser.add_argument('adopted', type=bool)
        parser.add_argument('sex', type=str)
        parser.add_argument('color', type=str)
        parser.add_argument('age-day', type=str)
        parser.add_argument('age-month', type=str)
        parser.add_argument('age-year', type=str)
        data = parser.parse_args()
        user_json = get_jwt_identity()
        cat = CatModel.findCatsByCatname(catname)
        if cat and cat.owner_id != user_json['user-id']:
            return { 'message': "Not permitted action" }, 401
        elif cat and cat.owner_id == user_json['user-id']:
            if data['name']:
                cat.name = data['name']
            if data['img_url']:
                cat.img_url = data['img_url']
            if data['adopted']:
                cat.adopted=data['adopted']
            if data['sex']:
                cat.sex = data['sex']
            if data['color']:
                cat.color = data['color']
            if data['age-day']:
                cat.ageD = data['age-day']
            if data['age-month']:
                cat.ageM = data['age-month']
            if data['age-year']:
                cat.ageY = data['age-year']
            cat.saveToDB()
            return cat.json()
        else:
            return { 'message': 'cat not found'}, 404


    @jwt_required
    def delete(self,catname):
        cat = CatModel.findCatsByCatname(catname)
        user_json = get_jwt_identity()
        if cat and (cat.owner_id == user_json['user-id'] or user_json['admin'] == True):
            cat.deleteFromDB()
            return { 'message': 'cat was deleted successfully' }, 202
        elif cat and cat.owner_id != user_json['user-id']:
            return { 'message': 'You must be the original owner to delete this cat' }
        return { 'message': 'cat not found' }, 404

class ListCats(Resource):
    def get(self):
        return { 'cats': [cat.json() for cat in CatModel.query.all()]}

class ListAdoptedCats(Resource):
    def get(self):
        return { 'adopted-cats': [cat.json() for cat in CatModel.query.all() if cat.adopted == True] }


class IsAdopted(Resource):
    # improve this function to indicate the name of the adopter
    def get(self, catname):
        cat = CatModel.findCatsByCatname(catname)
        if cat:
            if cat.adopted:
                from models.user import UserModel
                adopter = UserModel.findUserById(cat.adopter_id)
                return { 'message': 'This cat is adopted by {}'.format(adopter.firstName + ' ' + adopter.lastName) }, 200
            else:
                return { 'message': 'This cat is not adopted by anyone. Please adopt it'}, 200
        else:
            return { 'message': 'Could not find the requested cat'}, 404

class TakenCatname(Resource):
    def get(self, catname):
        cat = CatModel.findCatsByCatname(catname)
        if cat:
            return { 'taken': True }, 400
        return {'taken': False}
