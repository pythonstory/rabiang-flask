page, article, journal, post, document, messages



URI

blog

/page : page list
/page/tag : tag list
/page/tag/<slug> : page list with tag
/page/user/<username> : page list with username
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
/auth/register
/auth/unregister


basic methods

index
detail
create
edit
delete

import

always use absolute package path but relative path for current directory


- form valid error
- slug unique check
- form label - i18n
- date formatting (posted on, modified on)
- breadcrumbs / trailers
- pagination : parameterized
- babel select lang html

- comments
- widget MVC
- blueprint dynamic import
- import (circular?)

- user authentication
- registration
- email confirmation
- storing password
- forgot password
