# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


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
        perm = Permission.query \
            .filter(Permission.name == permission) \
            .first()

        if not perm:
            return

        return RolePermissionResource.query \
            .join(Role) \
            .join(User) \
            .join(Resource) \
            .filter((User.id == self.id) &
                    (Resource.name == resource) &
                    (RolePermissionResource.permission.op('&')
                     (perm.bit) == perm.bit)) \
            .first()

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User: %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    @staticmethod
    def can(resource, permission):
        perm = Permission.query \
            .filter(Permission.name == permission) \
            .first()

        if not perm:
            return

        return RolePermissionResource.query \
            .join(Role) \
            .join(Resource) \
            .filter((Role.name == 'Anonymous') &
                    (Resource.name == resource) &
                    (RolePermissionResource.permission.op('&')
                     (perm.bit) == perm.bit)) \
            .first()


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
        admin_role = Role(name='Admin')
        db.session.add(admin_role)

        anonymous_role = Role(name='Anonymous')
        db.session.add(anonymous_role)

        user = User(username='test', email='test@example.com', password='test',
                    active=True, role=admin_role)
        db.session.add(user)

        # anonymous_role is not assigned to a specific user.

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

        role_permission = RolePermissionResource(role=admin_role,
                                                 permission=11,
                                                 resource=resource)
        db.session.add(role_permission)

        role_permission = RolePermissionResource(role=anonymous_role,
                                                 permission=8,
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

        role_permission = RolePermissionResource(role=admin_role,
                                                 permission=11,
                                                 resource=resource)
        db.session.add(role_permission)

        role_permission = RolePermissionResource(role=anonymous_role,
                                                 permission=3,
                                                 resource=resource)
        db.session.add(role_permission)

        db.session.commit()

    def __init__(self, *args, **kwargs):
        super(RolePermissionResource, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<RolePermissionResource: %r on %r>' \
               % (self.role.name, self.resource.name)
