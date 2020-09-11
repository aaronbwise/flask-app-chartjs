from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '7f90408af1b0e368ac19c775e5e892ef'

# Value to switch between development and production
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    # development database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:P@ssw1rd@localhost/budget'
else:
    # deployment database
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database instance
db = SQLAlchemy(app)
# Create bcrypt instance
bcrypt = Bcrypt(app)
# Create loginmanager instance
login_manager = LoginManager(app)

from budgetapp import routes
