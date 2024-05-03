from sqlalchemy import UniqueConstraint
from dataclasses import dataclass
from app import db

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductsUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    # TODO: not working actually
    UniqueConstraint(user_id, product_id, name='user_product_unique')

@dataclass
class User(db.Model):
    id: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)