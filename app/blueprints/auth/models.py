# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.now,
                                   onupdate=datetime.now)


class User(UserMixin, Base):
    __tablename__ = 'user'

    username = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role',
                           backref=db.backref('users', lazy='dynamic'))

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        # password field is hidden and not added even on the table.
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def can(self, resource=None, permission=None):
        p = Permission.query \
            .filter(Permission.name == permission) \
            .first()

        if not p:
            return

        return RolePermissionResource.query \
            .join(Role) \
            .join(User) \
            .join(Resource) \
            .filter((User.id == self.id) &
                    (Resource.name == resource) &
                    (RolePermissionResource.permission.op('&')(p.bit) ==
                     p.bit)) \
            .first()

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User: %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, resources, permissions):
        return False

    def is_administrator(self):
        return False


class Role(Base):
    __tablename__ = 'role'

    name = db.Column(db.String(64))

    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Role: %r>' % self.name


class Resource(Base):
    __tablename__ = 'resource'

    name = db.Column(db.String(64))

    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Resource: %r>' % self.name


class Permission(Base):
    __tablename__ = 'permission'

    name = db.Column(db.String(64))
    bit = db.Column(db.Integer)

    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    resource = db.relationship('Resource',
                               backref=db.backref('permissions',
                                                  lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Permission, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Permission: %r>' % self.name


class RolePermissionResource(Base):
    __tablename__ = 'role_permission_resource'

    permission = db.Column(db.Integer)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role',
                           backref=db.backref('permissions', lazy='dynamic'))

    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    resource = db.relationship('Resource',
                               backref=db.backref('role_permissions',
                                                  lazy='dynamic'))

    @staticmethod
    def insert_role_permission():
        role = Role(name='admin')
        db.session.add(role)

        user = User(username='test', email='test@example.com', password='test',
                    active=True, role=role)
        db.session.add(user)

        resource = Resource(name='post')
        db.session.add(resource)
        permission = Permission(name='create', bit=1, resource=resource)
        db.session.add(permission)
        permission = Permission(name='edit', bit=2, resource=resource)
        db.session.add(permission)
        permission = Permission(name='delete', bit=4, resource=resource)
        db.session.add(permission)
        permission = Permission(name='view', bit=8, resource=resource)
        db.session.add(permission)

        role_permission = RolePermissionResource(role=role, permission=11,
                                                 resource=resource)

        db.session.add(role_permission)

        resource = Resource(name='auth')
        db.session.add(resource)
        permission = Permission(name='register', bit=1, resource=resource)
        db.session.add(permission)
        permission = Permission(name='login', bit=2, resource=resource)
        db.session.add(permission)
        permission = Permission(name='manage', bit=4, resource=resource)
        db.session.add(permission)

        role_permission = RolePermissionResource(role=role, permission=11,
                                                 resource=resource)
        db.session.add(role_permission)

        db.session.commit()

    def __init__(self, *args, **kwargs):
        super(RolePermissionResource, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<RolePermissionResource: %r on %r>' \
               % (self.role.name, self.resource.name)


@login_manager.user_loader
def _user_loader(user_id):
    # User loader callback function
    return User.query.get(int(user_id))
