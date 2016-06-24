Template Structure

# Theme and Blueprints Folder

```
default/
    auth/
    page/
        index.html
        ...
    ...
    base.html
    columns-1.html
    columns-2.html
    breadcrumb.html
    navigation.html
    sidebar.html
    404.html
    500.html
```

```default``` folder is the name of default theme. You can create another theme folder and its structure as listed above.

```default``` folder has sub folders which are blueprints.

# Inheritance and Composition

## Inheritance

* ```page/create.html```(content page) extends ```columns-2.html```(layout page).
* ```columns-2.html``` extends ```base.html```(theme page).

### Block Definitions

* ```base.html``` has block ```title```, ```extra_styles```, ```layout``` and ```extra_scripts```.
* ```column-2.html``` has block ```page_content```, and defines block ```layout```
* ```page/create.html``` defines ```title```, ```page_content```, ```extra_styles``` and ```extra_scripts```.

## Composition

* ```columns-2.html``` includes ```sidebar.html```.
* ```base.html``` includes ```navigation.html``` and ```breadcrumb.html```.

## Inclusion

Files starting with underscore(_) is included in content page.

```page/index.html``` includes ```page/_post_list.html``` and ```page/_pagination.html```.
