# pyrefly: ignore [missing-import]
from flask import Flask
from config import Config
from extension import db, jwt, bcrypt, cors


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    from models.user import User
    from models.product import Product
    from models.cart import Cart, CartItem
    from models.order import Order
    from models.order_item import OrderItem
    from routes.products import products_bp
    from routes.cart import cart_bp
    from routes.auth import auth_bp

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)

    @app.route("/")
    def home():
        return {"message": "Shopping Backend"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)