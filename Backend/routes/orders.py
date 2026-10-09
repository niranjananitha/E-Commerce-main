# pyrefly: ignore [missing-import]
from flask import Blueprint,jsonify
# pyrefly: ignore [missing-import]
from flask_jwt_extended import jwt_required , get_jwt_identity

from extension import db
from models.cart import Cart, CartItem
from models.product import Product
from models.order import Order
from models.order_item import OrderItem

orders_bp=Blueprint("orders",__name__,url_prefix="/api/orders")


@orders_bp.route("/",methods=["POST"])
@jwt_required()
def create_order():

    user_id= get_jwt_identity()

    cart=Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return jsonify({
            "message":"Cart Not Found"
        }),404
    cart_items=CartItem.query.filter_by(cart_id=cart.id).all()

    if not cart_items:
        return jsonify({
            "message":"Cart is Empty"
        }),400
    
    
    total=0
    order_item_data=[]
    for item in cart_items:
        product=Product.query.get(item.product_id)
        if not product:
            return jsonify({
                "message":"Product not Found"
            }),404

        if item.quantity >product.stock:
            return jsonify({
                "message":f"Not enought stock for{product.name}"
            }),400
        subtotal=float(product.price)*item.quantity
        total+=subtotal
        order_item_data.append({
            "product_id":product.id,
            "quantity":item.quantity,
            "price":product.price
        })
        product.stock-=item.quantity
    order=Order(
        user_id=user_id,
        total_amount=total,
        status="Pending"
    )
    db.session.add(order)
    db.session.flush()
    

    for item_data in order_item_data:

        order_item=OrderItem(
            order_id=order.id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            price=item_data["price"]
        )
        db.session.add(order_item)
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    return jsonify({
        "message":"Order created Sucessfully",
        "order":{
            "id":order.id,
            "total_amount":float(order.total_amount),
            "status":order.status
        }
    }),201


@orders_bp.route("/",methods=["GET"])
@jwt_required()

def get_orders():

    user_id=get_jwt_identity()

    orders=Order.query.filter_by(
        user_id=user_id
    ).order_by(Order.created_at.desc()).all()

    order_list=[]

    for order in orders:

        order_items=OrderItem.query.filter_by(
            order_id=order.id
        ).all()

        item=[]

        for item in order_items:
            product=Product.query.get(item.product_id)

            item.append({
                "product_id": item.product_id,
                "name":product.name if product else "Product unavalable",
                "quantity":item.quantity,
                "price":float(item.price),
                "subtotal":float(item.price)*item.quanitity
            })
        order_list.append({
            "id":order.id,
            "total_amount":float(order.total_amount),
            "status":order.status,
            "items":item,
            "created_at":order.created_at.isoformat()
        })
    return jsonify({
        "orders":order_list
    }),200

@orders_bp.route("/<int:order_id>",method=["GET"])
@jwt_required()
def get_order(order_id):
    
    user_id=get_jwt_identity()

    order=Order.query.filter_by(
        id=order_id,
        user_id=user_id
    ).first()

    if not order:
        return jsonify({
            "message":"Order not Found"
        }),404
    
    order_items=OrderItem.query.filter_by(
        order_id=order.id
    ).all()

    item=[]

    for item in order_items:

        product=Product.query.get(item.product_id)

        item.append({
            "product_id":item.product_id,
            "name": product.name if product else "Product unavailable",
            "quantity":item.quantity,
            "price": float(item.price),
            "subtotal": float(item.price)*item.quantity

        })

    