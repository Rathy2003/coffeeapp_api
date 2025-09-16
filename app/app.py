import os
from flask import send_from_directory,Blueprint
from flask_cors import CORS
from flask_migrate import Migrate
from api.category.category_v1 import category_bg
from api.product.product_v1 import product_bg
from extentions.extensions import db,app
from admin_page.views import admin_bp
from models.model import Category, Product,User,Role
from flask_security import Security, SQLAlchemyUserDatastore, hash_password

# must import to prevent error for app config
import app_config

from dotenv import load_dotenv
load_dotenv()

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

image_file_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
icon_file_path = os.path.join(os.path.dirname(__file__),'static','uploads','icons')

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# API Section
api_bp = Blueprint('api',__name__,url_prefix='/api')
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(image_file_path, filename)

# register blueprint
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(category_bg)
app.register_blueprint(product_bg)

# one time setup
with app.app_context():
    # Create User to test with
    db.create_all()
    if not security.datastore.find_user(email="admin@me.com"):
        security.datastore.create_user(username="admin",email="admin@me.com", password=hash_password("admin123"))
    db.session.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)