# -*- coding: utf-8 -*-
def build_tree_dictionary(node, model, level=0):
    children = node.children \
        .order_by(model.order.asc()) \
        .all()

    dic = {'node': node, 'level': level, 'children': []}

    if len(children) > 0:
        for child in children:
            dic['children'] \
                .append(build_tree_dictionary(child, model, level + 1))

    return dic
