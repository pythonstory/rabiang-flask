# Blueprints

URL mapping rules can be retrieved by ```app.url_map``` which is the instance of ```<class 'werkzeug.routing.Map'>```.

## main

/ : main.index : main.view

## auth

Authentication and Authorization

* /auth/change_password : change password form GET / save POST
* /auth/login : login form GET / login POST
* /auth/logout : logout GET
* /auth/permission
* /auth/permission/<resource>
* /auth/register : register form GET / save POST
* /auth/reset_password
* /auth/resource
* /auth/role
* /auth/role/user/<user_id>
* /auth/unregister : unregister form GET / delete POST

## page

Blog

* /page/ : page list
* /page/<post_id>
* /page/<slug> : detail
* /page/category
* /page/category/<category_name>/<page_num>
* /page/category/create
* /page/category/delete/<category_id>
* /page/category/edit/<category_id>
* /page/create: new page form GET / save POST
* /page/delete/<post_id> : delete page GET / delete POST
* /page/edit/<post_id> : edit page form GET / save POST
* /page/feed
* /page/month/<year>/<month>/<page_num>
* /page/tag : tag list
* /page/tag/<name> : page list with tag
* /page/user/<username> : page list with username

## forum

* /forum/<name>/index?page=7&q=keyword
* /forum/<name>/detail?id=9
* /forum/<name>/create
* /forum/<name>/edit?id=9
* /forum/<name>/delete?id=9
