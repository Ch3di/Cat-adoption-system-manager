from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    firstName = db.Column(db.String(40))
    lastName = db.Column(db.String(40))
    address = db.Column(db.String(80))
    password = db.Column(db.String(80))


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
        return { 'username': self.username, 'firstName': self.firstName, 'lastName': self.lastName, 'address': self.address, 'added-cats' : [], 'adopted-cats' : [] }

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
