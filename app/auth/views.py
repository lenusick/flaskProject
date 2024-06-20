from flask import render_template, redirect, session, url_for, request, flash
from app.auth.forms import *
from ..auth import auth
from app.models import *
from flask_mail import Message
from flask_login import current_user, logout_user, login_user, login_required
from .. import mail


@auth.route('/signin', methods=['GET', 'POST'])
def sign_in():
    '''
    Функция аутентифицирует и авторизует текущего пользователя, проверяя его данные,
    устанавливает сессию и перенаправляет на следующую страницу
    '''
    if not current_user.is_authenticated:
        form = AvtorizatziyaForm()
        if form.validate_on_submit():
            user = User.query.filter_by(login=form.login.data).first()
            if user is not None and user.password_verify(form.password.data):
                login_user(user)
                session['login'] = form.login.data
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
            flash('Что-то пошло не так')
        return render_template("loginForm.html", form=form)
    return redirect('/')


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    '''
    Функция проверяет аутентификацию пользователя, создает и валидирует форму регистрации,
    добавляет данные в базу, генерирует токен подтверждения, и перенаправляет на главную страницу.
    Если пользователь не аутиентифицирован, то перенаправляет на главную
    '''
    if not current_user.is_authenticated:
        form = RegistratziyaForm()
        if form.validate_on_submit():
            user = User(login=form.login.data,
                        email=form.email.data,
                        password=form.password.data,
                        sex=form.sex.data,
                        role=Role.query.get(form.role.data))
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            # confirm(form.login.data, form.email.data, token.decode('utf-8'))
            return redirect('/')
        return render_template('baseFormTemplate.html', form=form)
    return redirect('/')


@auth.route('/logout')
def log_out():
    '''
    Функция очищает сессию пользователя, выполняет выход из системы
    и перенаправляет на главную страницу
    '''
    session['login'] = ""
    logout_user()
    return redirect('/')


def confirm(name, email, token):
    '''
    Функция принимает три аргумента: name, email и token.
    Затем она вызывает функцию send_mail(), передавая в нее
    адрес электронной почты, тему письма, шаблон письма и параметры name и token
    '''
    send_mail(email, 'If you wonder', 'mailTemplate', name=name, token=token)


def send_mail(to, subject, template, **kwargs):
    '''
    Функция создает объект сообщения (`msg`),
    устанавливает тему (`subject`) и отправителя, добавляет получателя (`to`),
    формирует тело сообщения, используя текстовый шаблон (`template`) и переданные аргументы (`kwargs`),
    и затем отправляет сообщение (`mail.send`)
    '''
    msg = Message(subject, sender="lminlisa@gmail.com",
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    mail.send(msg)


@auth.route('/check/<token>')
@login_required
def check_token(token):
    '''Функция обрабатывает запрос на проверку токена подтверждения пользователя,
    проверяет подтверждение текущего пользователя,
    подтверждает пользователя с использованием токена,
    фиксирует изменения в базе данных, отображает сообщение пользователю
    и перенаправляет его на главную страницу
    '''
    if current_user.confirmed:
        return redirect('/')
    if current_user.confirm(token):
        db.session.commit()
        flash('Подтверждение прошло успешно!')
    else:
        flash('Подтверждение не прошло(')
    return redirect(url_for('main.index'))
