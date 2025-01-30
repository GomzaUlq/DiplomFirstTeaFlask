from email_validator import validate_email
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Имя', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6),
        EqualTo('confirm_password', message='Пароли должны совпадать.')
    ])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        if not validate_email(field.data):
            raise ValidationError('Некорректный email адрес.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Этот логин уже занят.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Этот email уже используется.')


class CheckoutForm(FlaskForm):
    address = StringField('Адрес:', validators=[DataRequired()])
    phone = StringField('Номер телефона:', validators=[DataRequired()])
    submit = SubmitField('Подтвердить заказ')