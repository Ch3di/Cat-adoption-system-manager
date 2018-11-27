from db import db
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable = False)
    firstName = db.Column(db.String(40))
    lastName = db.Column(db.String(40))
    address = db.Column(db.String(80))
    password = db.Column(db.String(80), nullable = False)
    cats = db.relationship('CatModel', lazy='dynamic')

    def __init__(self, username, firstName, lastName, address, password):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.password = password

    @classmethod
    def findUserByUsername(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def findUserById(cls, id):
        return cls.query.filter_by(id=id).first()

    def json(self):
        return { 'user-id': self.id ,'username': self.username, 'firstName': self.firstName, 'lastName': self.lastName, 'address': self.address, 'added-cats' : [cat.json() for cat in self.cats.all()], 'adopted-cats' : [] }

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def generateHash(password):
        return sha256.hash(password)

    @staticmethod
    def verifyHash(password, hash):
        return sha256.verify(password, hash)
