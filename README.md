# Flask-boilerplate

## Requirements

* Flask
* Flask-script
* Flask-SQLAlchemy
* Flask-WTP
* Flask-Babel

## Features

* Custom config file support
    * ```config_production.py``` for production
    * ````config_testing.py``` for testing
* Structure with blueprint
    * templates and static folders
    * theme supported
* AlloyUI support
* i18n / l10n support
* Unit Test
* Logging support

## Configuration and Run

It is not recommended to use ```config.py``` for your production server.

You have to have your own config file such as ```config_production.py```, and you can run as shown below:

```
python manage.py -c config_production runserver
```

If you not specify ```-c``` option, it will import the default ```config.py```.

## Commands

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
