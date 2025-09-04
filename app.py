import os

from flask import Flask, jsonify, request, send_from_directory
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_admin.form import ImageUploadField, Select2Widget
from flask_migrate import Migrate
from flask_admin import Admin
from markupsafe import Markup
from admin import MyAdminIndexView, SecureModelView
from extensions import basic_auth,db
from models.model import Category, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/coffeeapp_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended to set to False
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

app.config['SECRET_KEY'] = '6001136d23c7f17bba45b895502ef05aab605bcde4397f98fc093e0e89534814'

basic_auth.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

file_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

class ProductAdmin(SecureModelView):
    column_list = ('name', 'price', 'description','category','image')
    form_extra_fields = {
        'image': ImageUploadField('image',base_path=file_path,url_relative_path="uploads/"),
        'category': QuerySelectField(
            'Category',
            query_factory=lambda: Category.query.all(),
            get_label='name',
            widget=Select2Widget(),
        )
    }

    column_formatters = {
        'image': lambda v, c, m, p: Markup(
            f'<img src="/uploads/{m.image}" style="max-height: 100px;">'
        ) if m.image else '',
        'category': lambda v, c, m, p: Markup(
            f'<span>{m.category.name}</span>'
        )
    }


admin = Admin(app,index_view=MyAdminIndexView(),template_mode="bootstrap3")
admin.add_view(SecureModelView(Category, db.session))
admin.add_view(ProductAdmin(Product, db.session))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(file_path, filename)
@app.route("/api/category", methods=["GET","POST"])
def category_api():
    if request.method == "GET":
        categories = Category.query.order_by(Category.id).all()
        return jsonify([cat.to_dict() for cat in categories])
    else:
        name = request.form.get("name")
        category = Category(name)

        return jsonify({"message":"Category has been created"})


if __name__ == "__main__":
    app.run(debug=True)


