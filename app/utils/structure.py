# -*- coding: utf-8 -*-
def get_children(model, node):
    if node is None:
        return model.query \
            .filter(model.parent_id == None) \
            .order_by(model.order.asc()) \
            .all()
    else:
        return node.children \
            .order_by(model.order.asc()) \
            .all()


def build_tree_dictionary(model, node=None, level=0):
    children = get_children(model, node)

    dic = {'node': node, 'level': level, 'children': []}

    if len(children) > 0:
        for child in children:
            dic['children'] \
                .append(build_tree_dictionary(model, child, level + 1))

    return dic


def build_tree_list(model, node=None):
    children = get_children(model, node)

    tree = children

    if len(children) > 0:
        for child in children:
            tree.extend(build_tree_list(model, child))

    return tree


def build_tree_tuple_list(model, node=None, level=0, prefix=False):
    children = get_children(model, node)

    tree = []

    if len(children) > 0:
        for child in children:
            """
            If prefix is set for select option, it is indented with prefix.
            Otherwise, tuple list is returned with depth level.
            """
            if prefix:
                tree.append((child.id, '----' * level + child.name))
                tree.extend(
                    build_tree_tuple_list(model, child, level + 1, True))
            else:
                tree.append((child.id, child.name, level))
                tree.extend(build_tree_tuple_list(model, child, level + 1))

    return tree
