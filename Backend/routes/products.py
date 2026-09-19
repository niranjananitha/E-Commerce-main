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



@products_bp.route("/<int:product_id>",methods=["GET"])
def get_product(product_id):
    product=Product.query.get(product_id)

    if not product:
        return jsonify({
            "message":"Product not Found"
        }),404
    return jsonify({
        "product":{
            "id":product.id,
            "name":product.name,
            "description":product.description,
            "price":float(product.price),
            "category":product.category,
            "stock":product.stock,
            "image_url":product.image_url
        }
    }),200

@products_bp.route("/<int:product_id>",methods=["PUT"])
@jwt_required()
def update_product(product_id):
    product=Product.query.get(product_id)

    if not product:
        return jsonify({
            "message":"Product not found"
        }),404
    data=request.get_json()

    name=data.get("name")
    description=data.get("description")
    price=data.get("price")
    category=data.get("category")
    stock=data.get("stock")
    image_url=data.get("image_url")

    if not name or price is None or not category or stock is None :
        return jsonify({
            "message":"Name , price , category and stock are requried "
        }),400
    
    product.name=name
    product.description=description
    product.price=price
    product.category=category
    product.stock=stock
    product.image_url=image_url
    
    db.session.commit()
    return jsonify({
        "message":"Product updated successfully",
        "product":{
            "id":product.id,
            "name":product.name,
            "description":product.description,
            "price":float(product.price),
            "category":product.category,
            "stock":product.stock,
            "image_url":product.image_url
        }
    }),200

@products_bp.route("/<int:product_id>",methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    product=Product.query.get(product_id)

    if not product:
        return jsonify({
            "message":"Product not found"
        }),404
    db.session.delete(product)
    db.session.commit()
    return jsonify({
        "message":"Product deleted Sucessfully"
    }),200