# pyrefly: ignore [missing-import]
from flask import Blueprint, request, jsonify
# pyrefly: ignore [missing-import]
from flask_jwt_extended import jwt_required , get_jwt_identity

from extension import db 
from models.cart import Cart , CartItem
from models.product import Product

cart_bp=Blueprint(
    "cart",
    __name__,
    url_prefix="/api/cart"
)

@cart_bp.route("/items",methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id=get_jwt_identity()
    data=request.get_json()
    product_id=data.get("product_id")
    quantity=data.get("quantity",1)

    if product_id is None:
        return jsonify({
            "message":"product_id is Requried"
        }),400
    if quantity<=0:
        return jsonify({
            "message":"Quantity must be Greater than 0"
        }),400
    
    product =Product.query.get(product_id)

    if not product:
        return jsonify({
            "message":"Product not found"
        }),404
    cart=Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart=Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    cart_item=CartItem.query.filter_by(cart_id=cart.id,product_id=product_id).first()
    if cart_item:
        new_quanity=cart_item.quantity+quantity
        if new_quanity >product.stock:
            return jsonify({
                "message":"Not Enough stock for request quantity"
            }),400
        cart_item.quantity=new_quanity
    else:
        cart_item=CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({
        "message":"Item added to cart successfully",
        "cart_item":{
            "id":cart_item.id,
            "product_id":cart_item.product_id,
            "quantity":cart_item.quantity
        }
    }),201

@cart_bp.route("/", methods=["GET"])
@jwt_required()
def get_cart():

    user_id = get_jwt_identity()

    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return jsonify({
            "cart": {
                "id": None,
                "items": [],
                "total": 0
            }
        }), 200

    cart_items = CartItem.query.filter_by(
        cart_id=cart.id
    ).all()

    items = []
    total = 0

    for item in cart_items:

        product = Product.query.get(item.product_id)

        subtotal = float(product.price) * item.quantity

        items.append({
            "product_id": product.id,
            "name": product.name,
            "price": float(product.price),
            "quantity": item.quantity,
            "subtotal": subtotal
        })

        total += subtotal

    return jsonify({
        "cart": {
            "id": cart.id,
            "items": items,
            "total": total
        }
    }), 200


@cart_bp.route("/items/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_cart_item(product_id):

    user_id = get_jwt_identity()

    data = request.get_json()
    quantity = data.get("quantity")

    if quantity is None:
        return jsonify({
            "message": "Quantity is required"
        }), 400

    if quantity <= 0:
        return jsonify({
            "message": "Quantity must be greater than 0"
        }), 400

    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return jsonify({
            "message": "Cart not found"
        }), 404

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id
    ).first()

    if not cart_item:
        return jsonify({
            "message": "Product not found in cart"
        }), 404

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    if quantity > product.stock:
        return jsonify({
            "message": "Not enough stock"
        }), 400

    cart_item.quantity = quantity

    db.session.commit()

    return jsonify({
        "message": "Cart item updated successfully",
        "cart_item": {
            "product_id": product.id,
            "name": product.name,
            "price": float(product.price),
            "quantity": cart_item.quantity,
            "subtotal": float(product.price) * cart_item.quantity
        }
    }), 200

@cart_bp.route("/items/<int:product_id>",methods=["DELETE"])
@jwt_required()
def remove_cart_item(product_id):
    user_id=get_jwt_identity()

    cart=Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({
            "message":"Cart not found"
        }),404
    
    cart_item=CartItem.query.filter_by(cart_id=cart.id,product_id=product_id).first()

    if not cart_item:
        return jsonify({
            "message":"Product is Not found in Cart"
        }),404
    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({
        "message":"Cart item deleted successfully"
    }),200

@cart_bp.route("/", methods=["DELETE"])
@jwt_required()
def clear_cart():

    user_id = get_jwt_identity()

    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return jsonify({
            "message": "Cart not found"
        }), 404

    cart_items = CartItem.query.filter_by(
        cart_id=cart.id
    ).all()

    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    return jsonify({
        "message": "Cart cleared successfully"
    }), 200