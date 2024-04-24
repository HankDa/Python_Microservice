from flask import Flask, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass

from producer import publish
import requests

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
    # TODO: not working actually
    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route('/api/products')
def index():
    # Fetch all products from the database
    products = Product.query.all() 
    # Return the list of products as a JSON response
    return jsonify(products)

@app.route('/api/products/<int:id>/like', methods=["POST"])
def like(id):
    '''
    like a product by random user provide by admin's api.
    then add a this user to ProductsUser table.
    '''
    # TODO: this part is not really reasonable the two services shoud not communicate directly?
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()

    try:
        productUser = ProductsUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        publish("product_liked", id)
    # exception might be triggered when it conflict the constrain.
    except:
        abort(400, 'You already liked this product')


    return jsonify({
        'message': 'success'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')