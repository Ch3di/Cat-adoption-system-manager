from db import db


class CatModel(db.Model):
    __tablename__ = 'cats'
    cat_id = db.Column(db.Integer, primary_key=True)
    catname = db.Column(db.String(80))
    name = db.Column(db.String(80))
    img_url = db.Column(db.String(256))
    adopted = db.Column(db.Boolean)
    sex = db.Column(db.CHAR)
    ageD = db.Column(db.Integer)
    ageM = db.Column(db.Integer)
    ageY = db.Column(db.Integer)
    color = db.Column(db.String(80))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    adopter_id = db.Column(db.Integer)
    user = db.relationship('UserModel')

    def __init__(self, catname, owner_id, name, img_url, adopted, sex, color, ageD=0, ageM=0, ageY=0):
        self.catname = catname
        self.name = name
        self.img_url = img_url
        self.adopted = adopted
        self.sex = sex
        self.color = color
        self.owner_id = owner_id
        self.adopter_id = None
        self.ageD = ageD
        self.ageM = ageM
        self.ageY = ageY

    def json(self):
        # don't forget to add owner_id to json
        from models.user import UserModel
        owner = UserModel.findUserById(self.owner_id)
        if self.adopted:
            adopter = UserModel.findUserById(self.adopter_id)
            return {
                self.catname: {
                    'name': self.name,
                    'img_url': self.img_url,
                    'adopted': self.adopted,
                    'sex': self.sex,
                    'color': self.color,
                    'age-day': self.ageD,
                    'age-month': self.ageM,
                    'age-year': self.ageY,
                    'owner-id': self.owner_id,
                    'owner-username': owner.username,
                    'owner-name': owner.firstName + ' ' + owner.lastName,
                    'adopter-id': self.adopter_id,
                    'adopter-username': adopter.username,
                    'adopter-name': adopter.firstName + ' ' + adopter.lastName
                }
            }
        return {
            self.catname: {
                'name': self.name,
                'img_url': self.img_url,
                'adopted': self.adopted,
                'sex': self.sex,
                'color': self.color,
                'age-day': self.ageD,
                'age-month': self.ageM,
                'age-year': self.ageY,
                'owner-id': self.owner_id,
                'owner-username': owner.username,
                'owner-name': owner.firstName + ' ' + owner.lastName
            }
        }

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

    def isAdopted(self):
        return cat.adopted
