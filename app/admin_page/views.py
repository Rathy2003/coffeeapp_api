import json
import os

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import logout_user
from flask_security import auth_required
from models.model import Category, Image, Product,User
from extentions.extensions import db,app

admin_bp = Blueprint(
    'admin_page',
    __name__,
    url_prefix='/0/admin',
    template_folder="templates",
    static_url_path="",
    static_folder="static"
)

@admin_bp.before_request
@auth_required()
def before_request():
    pass

@admin_bp.route('/')
def dashboard():
    total_categories = Category.query.order_by(Category.id).count()
    total_products = Product.query.order_by(Product.id).count()
    total_users = User.query.order_by(User.id).count()
    return render_template("index.html",
                           total_categories=total_categories,
                           total_products=total_products,
                           total_users=total_users
                           )
# Start Category

# GET and CREATE
@admin_bp.route('/category',methods=["GET","POST"])
def admin_category_page():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            # check name exists
            # db.one_or_404(Category().query.filter_by(name=name))

            # flash("Category with this name already exist","name")
            # return redirect(url_for("admin_page.admin_category_page"))

            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            flash("Category created successfully","success")
            return redirect(url_for("admin_page.admin_category_page"))

    categories = Category.query.order_by(Category.id).all()
    category_list = [cat.to_dict() for cat in categories]
    return render_template("categories/category.html",categories=category_list)

# EDIT AND UPDATE
@admin_bp.route('/category/<category_id>',methods=["GET","POST"])
def admin_category_page_edit(category_id):
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            category = Category.query.filter_by(id=category_id).first()
            category.name = name
            db.session.commit()
            flash("Category updated successfully","success")
            return redirect(url_for("admin_page.admin_category_page"))
    categories = Category.query.order_by(Category.id).all()
    category_list = [cat.to_dict() for cat in categories]
    category = Category.query.filter_by(id=category_id).first()

    return render_template("categories/category.html",categories=category_list,category=category)

# Delete Category
@admin_bp.route('/category/delete',methods=["POST"])
def delete_category():
    category_id = request.json.get("id")
    category = Category.query.filter_by(id=category_id).first()
    # check if has category and category has product
    if category and len(category.products) > 0:
        return jsonify({"success": False,"message":"Can't delete this category because it has product."})
    elif category and len(category.products) == 0:
        db.session.delete(category)
        db.session.commit()
        return  jsonify({"success": True,"message":"Category has been deleted"})
    return jsonify({"success": False,"message":"Somthing went wrong"})

# End Category


# Start Product
@admin_bp.route('/product',methods=["GET","POST"])
def admin_product_page():
    search_query = None
    page = request.args.get("page",1,type=int)
    per_page = 2
    if request.args.get("q"):
        search_query = request.args.get("q").strip()
        products = Product.query.filter(Product.name.icontains(search_query)).all()
    else:
        products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("products/index.html",products=products,search_query=search_query)

@admin_bp.route('/product/create',methods=["GET","POST"])
def admin_create_product_page():
    if request.method == "POST":
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()
        price = request.form.get("price")
        volume = request.form.get("volume")
        rating = request.form.get("rating")
        total_reviews = request.form.get("total_reviews")
        category_id = request.form.get("category_id")

        # check if name already exists
        exist_product = db.session.query(Product).filter_by(name=name).first()
        if exist_product:
            flash("Product with this name already exist","error")
            return jsonify({"success":True})
        image_list = request.files.getlist("image")

        if name and description and price and volume and rating and total_reviews and category_id:
            product = Product(name=name,description=description,price=price,volume=volume,rating=rating,total_reviews=total_reviews,category_id=category_id)
            db.session.add(product)
            db.session.commit()

            # save uploaded images and save image path to database
            for image in image_list:
                image.save(app.config["UPLOAD_FOLDER"]+"/"+image.filename)
                img = Image(image="uploads/"+image.filename,product_id=product.id)
                db.session.add(img)
                db.session.commit()
            flash("Product created successfully","success")
            return jsonify({"success":True,"message":"Product created successfully"})
        return jsonify({"success":False,"message":"All fields are required"})
    categories = Category.query.order_by(Category.id).all()
    return render_template("products/create.html",categories=categories)

# delete product
@admin_bp.route('/product/delete',methods=["POST"])
def admin_delete_product():
    product_id = request.json.get("id")
    product = Product.query.filter_by(id=product_id).first()
    image_list = Image.query.filter_by(product_id=product.id).all()

    # remove image from file system
    for image in image_list:
        image_file = os.path.join(app.config["UPLOAD_FOLDER"], image.image.split("/")[1])
        if os.path.isfile(image_file):
            os.remove(image_file)
        db.session.delete(image)
        db.session.commit()

    # remove product and image from database
    db.session.delete(product)
    db.session.commit()

    return jsonify({"success":True})

# End Product

@app.route('/0/auth/logout')
def auth_logout():
    logout_user()
    return redirect(url_for('security.login'))