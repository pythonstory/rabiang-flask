# Installation

# Configuration

This application provides ```test.cfg```, but it is totally not recommended to use it as your production server settings.

You **must** have your own config file such as ```production.cfg```.

# Run

## Windows

```
(venv) > SET FLASK_APP=run.py
(venv) > SET FLASK_CONFIG=production.cfg
(venv) > python -m flask run
```

## Linux

```
(venv) > export FLASK_APP=run.py
(venv) > export FLASK_CONFIG=production.cfg
(venv) > python -m flask run
```

## Additional Useful Commands

### dbinit

This command delete and create all tables. It must be run only for the first time.
