from flask import render_template, url_for, flash, redirect
from budgetapp import app
from budgetapp.forms import RegistrationForm, LoginForm
from budgetapp.models import User, Post

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
