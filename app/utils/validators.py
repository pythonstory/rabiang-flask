# -*- coding: utf-8 -*-

from wtforms import ValidationError


class Unique(object):
    def __init__(self, model, field, message='This element already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        # If form field and existing data field match, it doesn't check.
        if field.object_data == field.data:
            return

        check = self.model.query.filter(self.field == field.data).first()

        if check:
            raise ValidationError(self.message)
