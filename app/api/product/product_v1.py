from flask import Blueprint, jsonify
from models.model import Product


product_bg = Blueprint("product_api",__name__,url_prefix="/api/v1/products")

@product_bg.route("", methods=["GET"])
def product_api():
    products = Product.query.order_by(Product.id).all()
    return jsonify([product.to_dict() for product in products])


# fetch by category
@product_bg.route("/category/<category_id>", methods=["GET"])
def product_by_category_api(category_id):
    products = Product.query.filter_by(category_id=category_id).all()
    return jsonify([product.to_dict() for product in products])