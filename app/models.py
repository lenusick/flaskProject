from . import db, login_manager, admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from authlib.jose import JsonWebSignature


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    about = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN]
        }
        default_role = "User"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    def __repr__(self):
        return self.name


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(200))
    sex = db.Column(db.String(7))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    skills = db.relationship('Skill', backref='user')

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == "lminlisa@gmail.com":
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not able to read')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_verify(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        jws = JsonWebSignature()
        protected = {'alg': 'HS256'}
        payload = self.id
        secret = 'secret'
        return jws.serialize_compact(protected, payload, secret)

    def confirm(self, token):
        jws = JsonWebSignature()
        data = jws.deserialize_compact(s=token, key='secret')
        print(data)
        if data.payload.decode('utf-8') != str(self.id):
            print('It is not your token')
            return False
        else:
            self.confirmed = True
            db.session.add(self)
            return True

    def __repr__(self):
        return '<User %r>' % self.login


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin.add_view(ModelView(Skill, db.session))
admin.add_view(ModelView(User, db.session))
