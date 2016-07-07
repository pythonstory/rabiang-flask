# Installation

# Configuration

This application repository provides ```test.cfg```, but it is totally not recommended to use it as your production server settings.

You **must** have your own config file ```prod.cfg```. Otherwise, you may create ```dev.cfg``` for your development environment.

These names ```prod.cfg```, ```dev.cfg```, ```test.cfg``` cannot be changed.

This application tries to read them in order. Thus, ```prod.cfg``` file is the highest priority.  

* Windows

```
(venv) > SET FLASK_APP=run.py
```

* Linux

```
(venv) $ export FLASK_APP=run.py
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

```
(venv) > python -m flask test
```
