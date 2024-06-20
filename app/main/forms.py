from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from ..models import *


class SkillForm(FlaskForm):
    name = StringField('Название навыка: ', validators=[DataRequired()])
    about = StringField("Пояснение: ")
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    submit = SubmitField("Добавить")

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(user.id, user.login) for user in User.query.all()]