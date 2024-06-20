from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SkillForm(FlaskForm):
    name = StringField('Название навыка: ', validators=[DataRequired()])
    about = StringField("Пояснение: ")
    submit = SubmitField("Добавить")
