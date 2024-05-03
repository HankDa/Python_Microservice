from flask import Blueprint, abort, jsonify
from app.models import Product, ProductsUser, User
from producer import publish
import requests

from app import app, db

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
    random_user = User.query.order_by(db.func.random()).first()
    print(random_user.id)

    try:
        productUser = ProductsUser(user_id=random_user.id, product_id=id)
        db.session.add(productUser)
        db.session.commit()
        publish("product_liked", id)
    # exception might be triggered when it conflict the constrain.
    except:
        abort(400, 'You already liked this product')
        
    return jsonify({
        'message': 'success'
    })