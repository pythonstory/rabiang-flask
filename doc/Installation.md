# Installation

# Configuration and Environment Variable

This application provides ```test.cfg```, but it is totally not recommended to use it as your production server settings.

You **must** have your own config file such as ```production.cfg```.

* Windows

```
(venv) > SET FLASK_APP=run.py
(venv) > SET FLASK_CONFIG=production.cfg
```

* Linux

```
(venv) $ export FLASK_APP=run.py
(venv) $ export FLASK_CONFIG=production.cfg
```

# Build Translations

# Create Tables (```initdb```)

```initdb``` command deletes and creates all tables. It must be run only for the first time.

```
(venv) > python -m flask initdb
```

Please, double-check what you're doing.

# Run

```
(venv) > python -m flask run
```

# Additional Useful Commands

## Test
