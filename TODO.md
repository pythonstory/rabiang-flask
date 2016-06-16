page, article, journal, post, document, messages



URI

blog

/page : page list
/page/tag : tag list
/page/tag/<slug> : page list with tag
/page/<slug> : detail
/page/create: new page form GET / save POST
/page/edit/<int:id> : edit page form GET / save POST
/page/delete/<int:id> : delete page GET / delete POST

board

/forum/<name>/index?page=7&q=keyword
/forum/<name>/detail?id=9
/forum/<name>/create
/forum/<name>/edit?id=9
/forum/<name>/delete?id=9

cart

/shop/product/<slug>
/shop/brand
/shop/vendor
/shop/pay
/shop/cart
/shop/bookmark

/poll

/auth

/auth/login
/auth/logout


method

index
detail
create
edit
delete


- form valid error
- flash message
- slug unique check
- breadcrumbs / trailers
- pagination : parameterized
- page delete action