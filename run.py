from db import db
from app import app


@app.before_first_request # execute the following function before the first request
def create_tables():
    db.create_all()
    if UserModel.findUserByUsername('admin') is None:
        adminPassword = UserModel.generateHash('secretpass')
        admin = UserModel('admin','Admin','', '', adminPassword)
        admin.saveToDB()
        admin.makeUserAdmin()

db.init_app(app)
