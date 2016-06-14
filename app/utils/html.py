# -*- coding: utf-8 -*-
import re


def slugify(s):
    s = str.strip(s)
    return re.sub('[^\w]+', '-', s).lower()
