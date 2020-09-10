from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import *

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

posts = [
    {
        'author': 'Aaron Wise',
        'title': 'Post 1',
        'content': 'First post content',
        'date_posted': '09 September 2020'
    },
    {
        'author': 'Lindsey Wise',
        'title': 'Post 2',
        'content': 'Second post content',
        'date_posted': '10 September 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.user.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@app.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
