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
