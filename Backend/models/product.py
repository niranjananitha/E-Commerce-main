from extension import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __init__(self, name=None, description=None, price=None, category=None, stock=0, image_url=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.stock = stock
        self.image_url = image_url