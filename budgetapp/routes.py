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

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
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
