# Code/Naming Conventions

## Python3/Flask

### PEP8

* import
    * always use absolute package path but relative path for current directory
    * Module names from ```from``` are sorted in alphabetical order.

### Route and methods

Basic Structure

| Route | Function method | HTTP method |
|-------|-----------------|-------------|
| / | index | GET |
| /index | index | GET |
| /<unique_id> | detail | GET |
| /create | index | GET/POST |
| /edit/<unique_id> | edit | GET/POST |
| /delete/<unique_id> | index | GET/POST |

### Form Save or Edit Action

* Save from Empty Form

```python
@page.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # Create an empty form
    form = PostForm()

    if form.validate_on_submit():
        # Create an empty instance
        post = Post()
        
        # Set each field explicitly not using form.populate_obj(post)
        post.title = form.title.data
        ...

        db.session.add(post)
        db.session.commit()

        flash(gettext('You wrote a new post.'), 'success')
        return redirect(url_for('page.detail_slug', slug=post.slug))
        
    return render_template('/default/page/create.html',
        form=form)        
```

* Edit from Loaded Form

```python
@page.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    # Retrieve instance from database for modification
    post = Post.query.get_or_404(post_id)
    
    # Populates instance into form before rendering
    form = PostForm(obj=post)

    if form.validate_on_submit():
        # Set each field explicitly not using form.populate_obj(post)
        post.title = form.title.data
        ...

        db.session.add(post)
        db.session.commit()

        flash(gettext('You edited your post.'), 'success')
        return redirect(url_for('page.detail_slug', slug=post.slug))
        
    return render_template('/default/page/edit.html',
        form=form)        
```

## HTML

### Jinja2 Template

* Included template file name starts with prefix underscore(_).

## Javascript

## IDE

I use PyCharm Professional Edition in order to develop the Flask application. I recommend to use PyCharm Community Edition if your budget doesn't allow.

I often utilize the following features not provided by PyCharm Community Edition:

* Jinja2 Template engine syntax highlight
* Database/SQL

However, it is not a huge barrier to develop the Flask application with PyCharm Community Edition. Most of configurations are up to developers because Flask is a micro web framework.
