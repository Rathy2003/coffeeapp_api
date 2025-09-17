import os
from urllib.parse import quote_plus
from extentions.extensions import app

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{quote_plus(os.getenv('MYSQL_PASSWORD'))}"
    f"@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
)


# UPLOAD FOLDER
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

# DATABASE
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     f"mysql+pymysql://root:123456"
#     f"@localhost/coffeeapp_db"
# )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended to set to False

# FLASK SECURITY
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')