# -*- coding: utf-8 -*-
def build_tree_dictionary(model, node=None, level=0):
    if node is None:
        children = model.query \
            .filter(model.parent_id == None) \
            .all()
    else:
        children = node.children \
            .order_by(model.order.asc()) \
            .all()

    dic = {'node': node, 'level': level, 'children': []}

    if len(children) > 0:
        for child in children:
            dic['children'] \
                .append(build_tree_dictionary(model, child, level + 1))

    return dic
