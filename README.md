# Rabiang

This application is currently being developed so that the following features are supported.

We are planning on initial release in September or October 2016.

## Features

* Blog
    * WYSIWYG editor and Markdown
* Cart
* Authentication
* Role-based Access Control
* Custom config file support
    * ```config_production.py``` for production
    * ```config_testing.py``` for testing
* Structure with blueprint
    * templates and static folders
    * theme supported
* AlloyUI 3 support
    * Bootstrap 3
    * YUI 3
* i18n / l10n support
* Unit Test
* Logging support
* MIT License

## Requirements

Rabiang is based on Flask/Python3, and it requires the following packages:

* Flask
* Flask-script
* Flask-SQLAlchemy
* Flask-WTP
* Flask-Babel
* Flask-Login

### Configuration and Run

It is not recommended to use ```config.py``` for your production server.

You have to have your own config file such as ```config_production.py```, and you can run as shown below:

```
python manage.py -c config_production runserver
```

If you not specify ```-c``` option, it will import the default ```config.py```.

## Helper Commands

### runserver

### shell
