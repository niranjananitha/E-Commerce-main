# pyrefly: ignore [missing-import]
from flask import Blueprint, request, jsonify
# pyrefly: ignore [missing-import]
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from extension import db, bcrypt
from models.user import User


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    email=data.get('email')
    password=data.get('password')
    if not email or not password:
        return jsonify({"message":"Email and password are requried"}),400
    user=User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message":"Invalid Email and Password"}),401
    if not bcrypt.check_password_hash(user.password_hash,password):
        return jsonify({"message":"Invalid Email and Password"}),401
    
    #login sucessfully
    access_token=create_access_token(identity=str(user.id))
    return jsonify({"message":"Login Sucessfully",
    "Access_Token":access_token,
    "user":{
        "id": user.id,
        "name": user.name,
        "email": user.email
    }}),200

@auth_bp.route("/me",methods=["GET"])
@jwt_required()
def get_user():
    user_id=get_jwt_identity()
    user=User.query.get(user_id)
    if not user:
        return jsonify({"message":"user not found"}),404
    return jsonify({"user":{"id":user.id,"name":user.name,"email":user.email}}),200

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "message": "Name, email and password are required"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "Email already registered"
        }), 409

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        name=name,
        email=email,
        password_hash=password_hash
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }), 201