# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime
from flask_babel import format_datetime

from flask import request


def gravatar(email, size=100, default='identicon', rating='g'):
    if email is None:
        return '//placehold.it/64x64'

    if request.is_secure:
        url = 'https://secure.gravatar.com/avatar'
    else:
        url = 'http://www.gravatar.com/avatar'

    hashed = hashlib.md5(email.encode('utf-8')).hexdigest()

    return '{url}/{hashed}?s={size}&d={default}&r={rating}' \
        .format(url=url,
                hashed=hashed,
                size=size,
                default=default,
                rating=rating)


def monthly_format(format, year, month):
    dt = datetime(year, month, 1, 0, 0)
    return format_datetime(dt, format)
