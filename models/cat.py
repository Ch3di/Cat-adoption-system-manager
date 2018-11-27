from db import db
#from model.user import UserModel

class CatModel(db.Model):
    __tablename__ = 'cats'
    cat_id = db.Column(db.Integer, primary_key=True)
    catname = db.Column(db.String(80))
    name = db.Column(db.String(80))
    img_url = db.Column(db.String(256))
    adopted = db.Column(db.Boolean)
    sex = db.Column(db.CHAR)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self, catname, owner_id, name, img_url, adopted, sex):
        self.catname = catname
        self.name = name
        self.img_url = img_url
        self.adopted = adopted
        self.sex = sex
        self.owner_id = owner_id

    def json(self):
        # don't forget to add owner_id to json
        return { 'name': self.name, 'img_url': self.img_url, 'adopted': self.adopted, 'sex': self.sex }

    @classmethod
    def findCatsByName(cls,name):
        return cls.query.filter_by(name=name).all()

    @classmethod
    def findCatsByCatname(cls,catname):
        return cls.query.filter_by(catname=catname).first()

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
