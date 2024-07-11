from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.app_context().push()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from book_library_app import authors
from book_library_app import models
from book_library_app import db_manage_commends
from book_library_app import errors
