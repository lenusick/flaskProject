from app import mail
from flask import render_template, session, redirect
from app.main.forms import *
from . import main
from app.models import *
from app.decorators import *


@main.route('/')
def index():
    '''
    Функция маршрутизации возвращает HTML-шаблон страницы "index.html" с именем пользователя из сессии,
    предварительно вызвав метод вставки ролей Role.insert_roles()
    '''
    Role.insert_roles()
    user = User.query.filter_by(id=current_user.get_id()).first()
    return render_template("index.html", user=user)


@main.route('/500')
@main.errorhandler(500)
def internal_server_error():
    return render_template("error500.html"), 500


@main.route('/createNew', methods=['GET', 'POST'])
@permission_required(Permission.ADMIN)
def add_new():
    '''
    Функция обрабатывает запрос на создание нового навыка.
    Она требует разрешения администратора (@permission_required(Permission.ADMIN)),
    создает форму для ввода данных о навыке, валидирует их при отправке формы,
    создает новый навык на основе введенных данных и текущего пользователя,
    сохраняет его в базе данных, и затем перенаправляет пользователя
    на страницу просмотра всех навыков (redirect('/viewSkills'))
    '''
    if current_user.is_authenticated:
        form = SkillForm()
        if form.validate_on_submit():
            user = User.query.filter_by(id=current_user.get_id()).first()
            skill = Skill(name=form.name.data,
                          about=form.about.data,
                          user=User.query.get(form.user_id.data))
            db.session.add(skill)
            db.session.commit()
            return redirect('/viewSkills')
        return render_template('createNew.html', form=form)
    return redirect('/')


@main.route('/viewSkills')
def skills():
    '''
    Функция обрабатывает запрос по маршруту '/viewSkills',
    используя модель User для извлечения навыков конкретного пользователя,
    и возвращает HTML-шаблон allSkills.html, отображающий эти навыки
    '''
    user = User.query.filter_by(id=current_user.get_id()).first()
    skills = user.skills
    if user.role.name == "Administrator":
        skills = Skill.query.all()
    return render_template('allSkills.html', skills=skills)
