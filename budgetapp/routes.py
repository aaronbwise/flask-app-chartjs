import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from budgetapp import app, db, bcrypt
from budgetapp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from budgetapp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        result = User(user=form.user.data, email=form.email.data, password=hashed_password)
        db.session.add(result)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        result = User.query.filter_by(email=form.email.data).first()
        if result and bcrypt.check_password_hash(result.password, form.password.data):
            login_user(result, remember=form.remember.data)
            next_page = request.args.get('next') # takes to page before login
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful: check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# Function for generating/saving/returning picture (+resize) filename
def save_picture(form_picture):
    # Generate filename
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # _ is unused variable name
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resize uploaded picture
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Save
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.user = form.user.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.user.data = current_user.user
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
