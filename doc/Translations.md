# Translations

## Language Setup

This application provides Korean and English, but other languages can be supported by 3rd party or your contribution.

## Extract message strings

```
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot app
```

This application contains messages using```lazy_gettext``` function. Don't forget the option ```-k lazy_gettext```.

## Update message PO file

```
pybabel update -i messages.pot -d app/translations
```

## Compile message file

```
pybabel compile -d app/translations
```
