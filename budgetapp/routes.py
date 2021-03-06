import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, send_from_directory
from budgetapp import app, db, bcrypt
from budgetapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, DataEntryForm
from budgetapp.models import DataEntry, User, Post
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd


@app.route("/")
def landing_page():
    return render_template('landing_page.html')

@app.route("/home")
@login_required
def home():
    return render_template('home.html', title='Home')

def read_data():    # Function for getting chart data
    # Read in csv
    filepath = os.path.join(app.root_path, 'static/data', 'data.csv')
    df = pd.read_csv(filepath, encoding='utf-8')

    return df

@app.route("/chart")
@login_required
def chart():
    df = read_data()
    
    labels = df['Date'].to_list()
    values_1 = df['Liabilities'].to_list()
    values_2 = df['Assets'].to_list()
    values_3 = df['Net Worth'].to_list()

    legend_1 = 'Liabilities'
    legend_2 = 'Assets'

    return render_template('chart.html', values_1=values_1, values_2=values_2, labels=labels,
    legend_1=legend_1, legend_2=legend_2)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        result = User(user=form.user.data, email=form.email.data,
                      password=hashed_password)
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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('landing_page'))


def save_picture(form_picture):    # Function for generating/saving/returning picture (+resize) filename
    # Generate filename
    random_hex = secrets.token_hex(8)
    # _ is unused variable name
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

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
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/data_entry", methods=['GET', 'POST'])
@login_required
def data_entry():
    form = DataEntryForm()
    if form.validate_on_submit():
        result = DataEntry(date=form.date.data,
                           asset1=form.asset1.data, asset2=form.asset2.data)
        db.session.add(result)
        db.session.commit()
        flash('Data has been recorded!', 'success')
        return redirect(url_for('home'))
    return render_template('data_entry.html', title='Data Entry', form=form)