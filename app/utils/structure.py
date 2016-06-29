# -*- coding: utf-8 -*-
def build_tree_dictionary(model, node=None, level=0):
    if node is None:
        children = model.query \
            .filter(model.parent_id == None) \
            .order_by(model.name.asc()) \
            .all()
    else:
        children = node.children \
            .order_by(model.name.asc()) \
            .all()

    dic = {'node': node, 'level': level, 'children': []}

    if len(children) > 0:
        for child in children:
            dic['children'] \
                .append(build_tree_dictionary(model, child, level + 1))

    return dic


def build_tree_list(model, node=None):
    if node is None:
        children = model.query \
            .filter(model.parent_id == None) \
            .order_by(model.name.asc()) \
            .all()
    else:
        children = node.children \
            .order_by(model.name.asc()) \
            .all()

    tree = children

    if len(children) > 0:
        for child in children:
            tree.extend(build_tree_list(model, child))

    return tree


def build_tree_tuple_list(model, node=None, level=0):
    if node is None:
        children = model.query \
            .filter(model.parent_id == None) \
            .order_by(model.name.asc()) \
            .all()
    else:
        children = node.children \
            .order_by(model.name.asc()) \
            .all()

    tree = []

    if len(children) > 0:
        for child in children:
            tree.append((child.id, '   ' * level + child.name))
            tree.extend(build_tree_tuple_list(model, child, level + 1))

    return tree
