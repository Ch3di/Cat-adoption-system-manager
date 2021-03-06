from db import db
from passlib.hash import pbkdf2_sha256 as sha256
from models.cat import CatModel
class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable = False)
    firstName = db.Column(db.String(40))
    lastName = db.Column(db.String(40))
    address = db.Column(db.String(80))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(100), nullable = False)
    cats = db.relationship('CatModel', lazy='dynamic')
    admin =  db.Column(db.Boolean)

    def __init__(self, username, firstName, lastName, address, password, email=None, phone=None):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.password = password
        self.email = email
        self.phone = phone
        self.admin = False
    @classmethod
    def findUserByUsername(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def findUserById(cls, id):
        return cls.query.filter_by(id=id).first()

    def json(self):
        return {
            'user-id': self.id,
            'admin': self.admin,
            'username': self.username,
            'first-name': self.firstName,
            'last-name': self.lastName,
            'address': self.address,
            'email': self.email,
            'phone': self.phone,
            'added-cats' : [cat.json() for cat in self.cats.all()],
            'adopted-cats' : [cat.json() for cat in CatModel.query.all() if cat.adopter_id == self.id]
        }

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def makeUserAdmin(self):
        self.admin = True
        self.saveToDB()

    @staticmethod
    def generateHash(password):
        return sha256.hash(password)

    @staticmethod
    def verifyHash(password, hash):
        return sha256.verify(password, hash)
