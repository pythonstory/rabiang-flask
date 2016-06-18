# Code/Naming Conventions

## Python3/Flask

### PEP8

* import
    * always use absolute package path but relative path for current directory

### Route and methods

Basic Structure

| Route | Function method | HTTP method |
|-------|-----------------|-------------|
| / | index | GET |
| /index | index | GET |
| /<unique_id> | detail | GET |
| /create | index | GET/POST |
| /edit/<unique_id> | edit | GET/POST |
| /delete/<unique_id> | index | GET/POST |

## HTML

### Jinja2 Template

## Javascript