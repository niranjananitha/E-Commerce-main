# pyrefly: ignore [missing-import]
from flask_cors import CORS
# pyrefly: ignore [missing-import]
from flask_jwt_extended import JWTManager
# pyrefly: ignore [missing-import]
from flask_bcrypt import Bcrypt
# pyrefly: ignore [missing-import]
from flask_sqlalchemy import SQLAlchemy



db=SQLAlchemy()
jwt=JWTManager()
bcrypt = Bcrypt()
cors=CORS()

