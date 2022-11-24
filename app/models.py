from datetime import datetime

from app import db, app


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False)
    pasword = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<users {self.id}>"


# class Profiles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     old = db.Column(db.Integer)
#     city = db.Column(db.String(100))
#
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#
#     def __repr__(self):
#         return f"<profiles {self.id}>"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    data = db.Column(db.DateTime,default= datetime.utcnow)

    def __repr__(self):
        return f"<posts {self.id}>"


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<menu {self.id}>"

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish1 = db.Column(db.Integer,db.ForeignKey('menu.id'),nullable=True)
    dish2 = db.Column(db.Integer, db.ForeignKey('menu.id'),nullable=True)
    dish3 = db.Column(db.Integer, db.ForeignKey('menu.id'),nullable=True)
    dish4 = db.Column(db.Integer, db.ForeignKey('menu.id'),nullable=True)
    dish5 = db.Column(db.Integer, db.ForeignKey('menu.id'),nullable=True)
    amount = db.Column(db.Integer,nullable = False)

    def __repr__(self):
        return f"<orders {self.id}>"


def __repr__(self):
    return f"<menu {self.id}>"


with app.app_context():
    db.create_all()
