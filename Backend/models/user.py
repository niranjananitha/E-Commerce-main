from datetime import datetime
from extension import db
class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password_hash=db.Column(db.String(255),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    def __init__(self, name=None, email=None, password_hash=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.email = email
        self.password_hash = password_hash
    