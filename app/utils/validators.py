# -*- coding: utf-8 -*-
import re

from wtforms import ValidationError


class Unique(object):
    def __init__(self, model, field, message='This element already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        # If form field and existing data field match, it doesn't validate.
        if field.object_data == field.data:
            return

        check = self.model.query.filter(self.field == field.data).first()

        if check:
            raise ValidationError(self.message)


class StrongPassword(object):
    def __init__(self, message='Weak password'):
        self.message = message

    def __call__(self, form, field):
        check = re.match(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{6,20})', field.data)

        """
            (               # Start of group
            (?=.*\d)		# must contain one digit from 0-9
            (?=.*[a-z])		# must contain one lowercase characters
            (?=.*[A-Z])		# must contain one uppercase characters
            (?=.*\W)        # must contain one special symbols
            .               # match anything with previous condition checking
            {6,20}          # length at least 6 characters and maximum of 20
            )
        """

        if check is None:
            raise ValidationError(self.message)
