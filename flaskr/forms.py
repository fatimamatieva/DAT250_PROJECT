from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField,SubmitField, validators
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
        validators.Regexp(
             "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$",
            message="Password must have minimum eight characters, at least one uppercase letter, one lowercase letter and one number"
        )

    ])
    confirm_password = PasswordField('Confirm Password',[
        validators.DataRequired(message="Confirm password is required")
    ])
    submit = SubmitField('Register')

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
    submit = SubmitField('Login')


class ChangePassword(FlaskForm):
    password = PasswordField('Password', [
        validators.DataRequired(message="Password is required"),    
    ])
    new_password = PasswordField('New Password', [
        validators.DataRequired(message="New Password is required"),
        validators.EqualTo('confirm_new_password', message="Passwords must match"),
        validators.Regexp(
             "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$",
            message="Password must have minimum eight characters, at least one uppercase letter, one lowercase letter and one number"
        )
    
    ])
    confirm_new_password = PasswordField('Confirm New Password',[
        validators.DataRequired(message="Confirm new password is required")
    ])
    submit = SubmitField('Change Password')
