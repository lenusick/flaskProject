from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, SubmitField, EmailField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo
from ..models import User, Role


class RegistratziyaForm(FlaskForm):
    login = StringField("Введите логин: ", validators=[DataRequired()])
    email = EmailField('Введите почту: ', validators=[DataRequired()])
    password = PasswordField("Введите пароль: ", validators=[DataRequired()])
    password_conf = PasswordField("Подтвердите пароль: ",
                                  validators=[EqualTo('password', message='Пароли должны совпадать'), DataRequired()])
    sex = SelectField("Ваш пол: ", choices=[('m', 'Мужской'), ('f', 'Женский')])
    role = SelectField('Role', coerce=int, validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Такая почта уже зарегистрирована')

    def validate_name(self, field):
        if User.query.filter_by(login=field.data).first():
            raise ValidationError('Такое имя уже зарегистрировано')

    def __init__(self, *args, **kwargs):
        super(RegistratziyaForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.all()]


class AvtorizatziyaForm(FlaskForm):
    login = StringField('Введите логин: ', validators=[DataRequired()])
    password = PasswordField("Введите пароль: ", validators=[DataRequired()])
    submit = SubmitField("Авторизироваться")
