# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# from flaskr import db
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField,SubmitField, BooleanField, validators
from flaskr.db import get_db

        
class RegistrationForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email(), validators.Length(min=8, max=20)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('Confirm_password', message='Passwords must match')
        #TODO:
        #password policy? symbols/uppercase/lowercase
        # validators.Regexp(pattern)
    
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_password(self, password):
        upper_count = 0
        letter_count = 0
        numb_count = 0

        for i in password.data:
            if i.isalpha():
                letter_count += 1
            if i.isdigit():
                numb_count += 1
            if i.isupper():
                upper_count += 1

        if numb_count > 0 and upper_count > 0:
            return True
        else:
            raise ValueError('The password must have at least one number and one upper case letter')

    def validate_email(self, email):
        print(email.data)
        db = get_db()

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (email.data,)
        ).fetchone()
        if user:
            raise validators.ValidationError('Email is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ChangePassword(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email(), validators.Length(min=8, max=20)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('Confirm_password', message='Passwords must match')
        #TODO:
        #password policy? symbols/uppercase/lowercase
        # validators.Regexp(pattern)
    
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Change Password')

    def validate_password(self, password):
        upper_count = 0
        letter_count = 0
        numb_count = 0

        for i in password.data:
            if i.isalpha():
                letter_count += 1
            if i.isdigit():
                numb_count += 1
            if i.isupper():
                upper_count += 1

        if numb_count > 0 and upper_count > 0:
            return True
        else:
            raise ValueError('The password must have at least one number and one upper case letter')

            