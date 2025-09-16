from extentions.extensions import db
from flask_security.models import fsqla_v3 as fsqla

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    products = db.relationship('Product', back_populates='category')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "products": self.products
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    images = db.relationship('Image', back_populates='product')
    price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    total_reviews = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship("Category", back_populates="products")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "images": [image.image for image in self.images],
            "price": self.price,
            "volume": self.volume,
            "rating": self.rating,
            "total_reviews": self.total_reviews,
            "category_id": self.category_id,
        }
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(500), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship("Product", back_populates="images")

fsqla.FsModels.set_db_info(db)

class Role(db.Model, fsqla.FsRoleMixin):
    pass

class User(db.Model, fsqla.FsUserMixin):
    pass