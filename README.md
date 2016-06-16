# Rabiang

## Features

* Custom config file support
    * ```config_production.py``` for production
    * ````config_testing.py``` for testing
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

## Installation

### Requirements

* Flask
* Flask-script
* Flask-SQLAlchemy
* Flask-WTP
* Flask-Babel

### Translations

* Extract message strings

```
pybabel extract -F babel.cfg -o messages.pot app
```
 
 * Update message PO file

```
pybabel update -i messages.pot -d app/translations
```

* Compile message file

```
pybabel compile -d app/translations
```

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

## TODO

* Mail
* Flask-migrate
* db.create_all(), db.drop_all() command

## References

* Flask Web Development - Chapter 7, Miguel Grinberg, O'Reilly
* [How to Structure Large Flask Applications](https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications)
* [Modular Applications with Blueprints](http://flask.pocoo.org/docs/0.11/blueprints/#blueprints)
