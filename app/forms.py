from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=(DataRequired(), Email()))
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField('Confirme a Senha', 
                validators=(DataRequired(), EqualTo('password')))
    submit = SubmitField('Registrar-se')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Nome de usuário já existe.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('O e-mail já está registrado.')

class QuestionForm(FlaskForm):
    options = RadioField('Opções: ', validators=[DataRequired()], default=1)
    submit = SubmitField('Próxima')
