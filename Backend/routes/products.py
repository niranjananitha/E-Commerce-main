# pyrefly: ignore [missing-import]
from flask import Blueprint, request, jsonify
# pyrefly: ignore [missing-import]
from flask_jwt_extended import jwt_required
from extension import db
from models.product import Product


products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/api/products"
)

@products_bp.route("/",methods=["GET"])
def get_products():
    products=Product.query.all()

    Product_list=[]
    for product in products:
        Product_list.append({
            "id":product.id,
            "name":product.name,
            "description":product.description,
            "price":float(product.price),
            "category":product.category,
            "stock":product.stock,
            "image_url":product.image_url
        })
    return jsonify({
        "products":Product_list
    }),200

@products_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    data = request.get_json()

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    category = data.get("category")
    stock = data.get("stock")
    image_url = data.get("image_url")

    if not name or price is None or not category or stock is None:
        return jsonify({
            "message": "Name, price, category and stock are required"
        }), 400

    product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        stock=stock,
        image_url=image_url
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created successfully",
        "product": {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "category": product.category,
            "stock": product.stock,
            "image_url": product.image_url
        }
    }), 201