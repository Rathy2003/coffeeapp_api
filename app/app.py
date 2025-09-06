import os
from urllib.parse import quote_plus

from flask import Flask, jsonify, send_from_directory,Blueprint
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_admin.form import ImageUploadField, Select2Widget, FileUploadField
from flask_cors import CORS
from flask_migrate import Migrate
from flask_admin import Admin
from markupsafe import Markup
from admin import MyAdminIndexView, SecureModelView
from extensions import basic_auth,db
from models.model import Category, Product
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{quote_plus(os.getenv('MYSQL_PASSWORD'))}"
    f"@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended to set to False
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
basic_auth.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

image_file_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
icon_file_path = os.path.join(os.path.dirname(__file__),'static','uploads','icons')

class ProductAdmin(SecureModelView):
    column_list = ('name', 'price', 'description','category','image')
    form_extra_fields = {
        'image': ImageUploadField('image', base_path=image_file_path, url_relative_path="uploads/"),
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


api_bp = Blueprint('api',__name__,url_prefix='/api')
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(image_file_path, filename)


# API
@api_bp.route("categories", methods=["GET"])
def category_api():
    categories = Category.query.order_by(Category.id).all()
    return jsonify([cat.to_dict() for cat in categories])

@api_bp.route("products", methods=["GET"])
def product_api():
    products = Product.query.order_by(Product.id).all()
    return jsonify([product.to_dict() for product in products])
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



