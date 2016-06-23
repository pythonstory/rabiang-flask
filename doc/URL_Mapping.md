# Blueprints

## auth

Authentication and Authorization

/auth/login : login form GET / login POST
/auth/logout : logout GET
/auth/register : register form GET / save POST
/auth/unregister : unregister form GET / delete POST
/auth/change_password : change password form GET / save POST
/auth/reset_password

## page

Blog

/page/ : page list
/page/tag : tag list
/page/tag/<slug> : page list with tag
/page/user/<username> : page list with username
/page/<slug> : detail
/page/create: new page form GET / save POST
/page/edit/<int:id> : edit page form GET / save POST
/page/delete/<int:id> : delete page GET / delete POST

## main


## forum

/forum/<name>/index?page=7&q=keyword
/forum/<name>/detail?id=9
/forum/<name>/create
/forum/<name>/edit?id=9
/forum/<name>/delete?id=9
