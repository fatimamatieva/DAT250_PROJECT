# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# from flaskr import db
from wtforms import Form, StringField, PasswordField,SubmitField, BooleanField, validators


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"
        
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('Retype Password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Sign Up')


    # username = StringField('Username',
    #                        validators=[DataRequired(), Length(min=2, max=20)]) # Validators to provide a basic requirement for the username
    # email = StringField('Email', validators=[DataRequired(), Email()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password')])
    # submit = SubmitField('Sign Up')

#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('That username is already taken! Please try another username.')

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('That email already exists.')


class LoginForm(Form):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')