from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from budgetapp.models import User

class RegistrationForm(FlaskForm):
    user = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Custom validations
    def validate_user(self, user):
        result = User.query.filter_by(user=user.data).first()
        if result:
            raise ValidationError('That username is already taken.')
    
    def validate_email(self, email):
        result = User.query.filter_by(email=email.data).first()
        if result:
            raise ValidationError('That email is already taken.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    user = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # Custom validations
    def validate_user(self, user):
        if user.data != current_user.user:
            result = User.query.filter_by(user=user.data).first()
            if result:
                raise ValidationError('That username is already taken.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            result = User.query.filter_by(email=email.data).first()
            if result:
                raise ValidationError('That email is already taken.')

class DataEntryDummyForm(FlaskForm):
    date = DateField('Date', format='%m/%d/%Y', validators=[
        DataRequired()])
    asset1 = FloatField('Capital_One_360', validators=[DataRequired()])
    asset2 = FloatField('ForeignBank_Cash', validators=[DataRequired()])
    submit = SubmitField('Post Data')