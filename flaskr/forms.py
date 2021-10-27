# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# from flaskr import db
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField,SubmitField, BooleanField, validators
from flaskr.db import get_db

        
class RegistrationForm(FlaskForm):
    email = StringField('Email', [
        validators.DataRequired(message="Email is required"), 
        validators.Email(), 
        validators.Regexp('.*(@uis\.no)$', message="Invalid email. Use your student email")
    ])

    password = PasswordField('Password', [
        validators.DataRequired(message="Password is required"),
        validators.EqualTo('confirm_password', message="Passwords must match"),
        #TODO:
        #PASSWORD POLICY
        # validators.Regexp(
        #     "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        #     message="Password must have minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character"
        # )

    ])
    confirm_password = PasswordField('Confirm Password',[
        validators.DataRequired(message="Confirm password is required")
    ])
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
        db = get_db()

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (email.data,)
        ).fetchone()
        if user:
            raise validators.ValidationError('Email is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', [
        validators.DataRequired(message="Email is required"), 
        validators.Email(message="Incorrect username or password."), 
        validators.Regexp('.*(@uis\.no)$', message="Incorrect username or password.")
    ])

    password = PasswordField('Password', [validators.DataRequired(message="Password is required")])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ChangePassword(FlaskForm):
    password = PasswordField('Password', [
        validators.DataRequired(message="Password is required"),    
    ])
    new_password = PasswordField('New Password', [
        validators.DataRequired(message="New Password is required"),
        validators.EqualTo('confirm_new_password', message="Passwords must match"),
        #PASSWORD POLICY
        # validators.Regexp(
        #     "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        #     message="Password must have minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character"
        # )
    
    ])
    confirm_new_password = PasswordField('Confirm New Password',[
        validators.DataRequired(message="Confirm new password is required")
    ])
    submit = SubmitField('Change Password')

    def validate_new_password(self, new_password):
        upper_count = 0
        letter_count = 0
        numb_count = 0

        for i in new_password.data:
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
