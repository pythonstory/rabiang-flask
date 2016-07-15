# -*- coding: utf-8 -*-
import bleach


def clean_and_linkify(html):
    allowed_tags = ['a', 'span', 'strong', 'i', 'h1', 'h2', 'h3', 'h4', 'h5',
                    'h6', 'p', 'pre', 'div', 'blockquote', 'ul', 'ol', 'li',
                    'table', 'th', 'tr', 'td', 'thead', 'tbody', 'code', 'img']

    return bleach.linkify(bleach.clean(html,
                                       tags=allowed_tags,
                                       strip=True))
