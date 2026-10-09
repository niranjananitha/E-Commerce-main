
from datetime import datetime
from extension import db

class Order(db.Model):
    __tablename__="orders"

    id=db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id=db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    total_amount=db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    status=db.Column(
        db.String(50),
        nullable=False
    )

    created_at=db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
