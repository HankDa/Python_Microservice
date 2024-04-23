from crypt import methods
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass

# This creates a Flask application instance.
app = Flask(__name__)
# mysql://username:password@server/db
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#TODO: try to understand how it work. used to serialise list of Product objects.
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

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route('/api/products')
def index():
    # Fetch all products from the database
    products = Product.query.all() 
    # Return the list of products as a JSON response
    return jsonify(products)

@app.route('/api/products/<int:id>/like', methods=["POST"])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    return jsonify(req.json())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')