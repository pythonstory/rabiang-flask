# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, \
    flash, current_app
from flask_babel import gettext
from flask_login import login_required

from app.blueprints.auth.decorators import permission_required
from app.blueprints.page.forms import CategoryForm, DeleteCategoryForm
from app.blueprints.page.models import Post, PageCategory
from app.blueprints.page.views import page
from app.blueprints.page.views.sidebar import sidebar_data
from app.extensions import db
from app.utils.structure import build_tree_tuple_list, build_tree_dictionary, \
    build_tree_list


@page.route('/category', methods=['GET', 'POST'])
@permission_required('post', 'view')
def category_index():
    categories = build_tree_dictionary(PageCategory)

    title = gettext('Category') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': gettext('Category'),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/category_index.html',
        categories=categories,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/category/<category_name>', methods=['GET', 'POST'])
@page.route('/category/<category_name>/<int:page_num>', methods=['GET', 'POST'])
@permission_required('post', 'view')
def category_detail(category_name, page_num=1):
    category = PageCategory.query \
        .filter(PageCategory.name == category_name) \
        .first_or_404()

    categories = build_tree_list(PageCategory, category)

    # Lookup posts with specified category and its descendants.
    category_names = [category.name]
    category_names.extend([category.name for category in categories])

    posts = Post.query \
        .filter(Post.status == Post.STATUS_PUBLIC) \
        .join(PageCategory) \
        .filter(PageCategory.name.in_(category_names)) \
        .order_by(Post.created_timestamp.desc()) \
        .paginate(page_num,
                  current_app.config['RABIANG_POSTS_PER_PAGE'],
                  False)

    title = gettext('Category') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': gettext('Category'),
        'href': url_for('page.category_index'),
    }, {
        'text': category_name,
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/category_detail.html',
        title=title,
        posts=posts,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)


@page.route('/category/create', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'create')
def category_create():
    form = CategoryForm()

    categories = build_tree_tuple_list(PageCategory, prefix=False)
    form.parent.choices = [(0, gettext('Root Category'))]
    form.parent.choices.extend([(cid, '----' * level + name)
                                for cid, name, level in categories])

    if form.validate_on_submit():
        page_category = PageCategory()

        page_category.name = form.name.data
        page_category.order = form.order.data

        if form.parent.data == 0:
            page_category.parent_id = None
        else:
            page_category.parent_id = form.parent.data

        db.session.add(page_category)
        db.session.commit()

        flash(gettext('You added a new category.'), 'success')
        return redirect(url_for('page.category_create'))

    title = gettext('Add categories') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': gettext('Add categories'),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/category_create.html',
        form=form,
        title=title,
        breadcrumbs=breadcrumbs,
        categories=categories
    )


@page.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'create')
def category_edit(category_id):
    page_category = PageCategory.query.get_or_404(category_id)

    form = CategoryForm(obj=page_category)

    categories = build_tree_tuple_list(PageCategory, prefix=False)
    form.parent.choices = [(0, gettext('Root Category'))]
    form.parent.choices.extend([(cid, '----' * level + name)
                                for cid, name, level in categories])

    if form.validate_on_submit():
        # The self node can't be the parent.
        if form.parent.data != page_category.id:
            page_category.name = form.name.data
            page_category.order = form.order.data

            if form.parent.data == 0:
                page_category.parent_id = None
            else:
                page_category.parent_id = form.parent.data

            db.session.add(page_category)
            db.session.commit()

        flash(gettext('You updated the category.'), 'success')
        return redirect(url_for('page.category_edit', category_id=category_id))

    form.parent.data = page_category.parent_id if page_category.parent_id else 0

    title = gettext('Edit categories') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': '{} - {}'.format(gettext('Edit categories'),
                                 page_category.name),
        'href': False,
    }]

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/category_edit.html',
        form=form,
        category_id=category_id,
        title=title,
        breadcrumbs=breadcrumbs,
        categories=categories
    )


@page.route('/category/delete/<int:category_id>', methods=['GET', 'POST'])
@login_required
@permission_required('post', 'create')
def category_delete(category_id):
    page_category = PageCategory.query.get_or_404(category_id)

    form = DeleteCategoryForm()

    if form.validate_on_submit():
        db.session.delete(page_category)
        db.session.commit()

        flash(gettext('You deleted the category.'), 'success')
        return redirect(url_for('page.category_create'))

    title = gettext('Delete') + ' - ' + \
            current_app.config['RABIANG_SITE_NAME']

    breadcrumbs = [{
        'text': gettext('Home'),
        'href': url_for('main.index'),
    }, {
        'text': gettext('Blog'),
        'href': url_for('page.post_index'),
    }, {
        'text': '{} - {}'.format(gettext('Delete a category'),
                                 page_category.name),
        'href': False,
    }]

    sidebar = sidebar_data()

    return render_template(
        current_app.config['RABIANG_SITE_THEME'] + '/page/category_delete.html',
        form=form,
        page_category=page_category,
        title=title,
        breadcrumbs=breadcrumbs,
        sidebar=sidebar)
