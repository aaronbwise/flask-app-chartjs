from datetime import datetime
from budgetapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Not an additional column, just runs query in background
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.user}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class DataEntry(db.Model):
    __tablename__ = 'budgetData'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    asset1 = db.Column(db.Float(precision=2), nullable=False)
    asset2 = db.Column(db.Float(precision=2), nullable=False)

    def __repr__(self):
        return f"<id={self.id}, date={self.date}, asset1={self.asset1}, asset2={self.asset2}>"
