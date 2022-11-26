from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,TextAreaField
from wtforms.validators import Length,DataRequired,ValidationError,Email,EqualTo
from ama.models import User

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class MessageForm(FlaskForm):
    name = StringField(label='name',validators=[DataRequired()])
    message = TextAreaField(label='Ketik Pesan Disini',validators=[DataRequired()])
    submit = SubmitField()

class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        username = User.query.filter_by(username=username_to_check.data).first()
        if username:
            raise ValidationError('Username telah terdaftar!, silahkan coba username lain.')
    
    def validate_email(self,email_to_check):
        username = User.query.filter_by(email=email_to_check.data).first()
        if username:
            raise ValidationError('Email yang anda masukkan telah terdaftar!, silahkan coba email lain.')
        
    username = StringField(label='username',validators=[DataRequired()])
    email = StringField(label='email',validators=[DataRequired(),Email()])
    password = PasswordField(label='password',validators=[DataRequired(),Length(min=5),EqualTo('password_confirm',message='Passwords must match')])
    password_confirm = PasswordField(label='password_confirm',validators=[Length(min=5)])
    submit = SubmitField()