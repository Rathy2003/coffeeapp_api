from flask import Blueprint, jsonify
from models.model import Category

category_bg = Blueprint("category_api",__name__,url_prefix="/api/v1/categories")

@category_bg.route("", methods=["GET"])
def category_api():
    categories = Category.query.order_by(Category.id).all()
    return jsonify([cat.to_dict() for cat in categories])