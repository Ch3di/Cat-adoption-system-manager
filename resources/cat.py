from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

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

    @jwt_required
    def post(self,catname):
        if CatModel.findCatsByCatname(catname):
            return { 'message': 'This catname has already taken'}, 400
        data = Cat.parser.parse_args()
        user_json = get_jwt_identity()
        cat = CatModel(catname, user_json['user-id'], **data)
        cat.saveToDB()
        return cat.json(), 201

    @jwt_required
    def put(self,catname):
        data = Cat.parser.parse_args()
        user_json = get_jwt_identity()
        cat = CatModel.findCatsByCatname(catname)
        if cat and cat.owner_id == user_json['user-id']:
            cat.name=data['name']
            cat.img_url=data['img_url']
            cat.adopted=data['adopted']
            cat.sex = data['sex']
        elif cat and cat.owner_id != user_json['user-id']:
            return { 'message': 'This catname has already taken or permission denied' }, 400
        else:
            cat = CatModel(catname, user_json['user-id'], **data)
        cat.saveToDB()
        return cat.json()

    @jwt_required
    def delete(self,catname):
        cat = CatModel.findCatsByCatname(catname)
        user_json = get_jwt_identity()
        if cat and cat.owner_id == user_json['user-id']:
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
        return { 'adopted-cats': [cat.json() for cat in CatModel.query.all() if cat.adopted = True] }


class IsAdopted(Resource):
    # improve this function to indicate the name of the adopter
    def get(self, catname):
        cat = CatModel.findCatsByCatname(catname)
        if cat:
            if cat.adopted:
                return { 'message': 'This cat is adopted by {}'.format(cat.adopter_id) }, 200
            else:
                return { 'message': 'This cat is not adopted by anyone. Please adopt it'}, 200
        else:
            return { 'message': 'Couldn\'t find the requested cat'}, 404
