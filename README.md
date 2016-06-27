# Rabiang

Rabiang(ระเบียง) is a Thai word which means wooden terrace.

I always dream of developing software with a cup of coffee sitting on the terrace.

I am not good at web design, so I had to adopt themes from [startbootstrap.com](http://startbootstrap.com/) based on Bootstrap 3.

Feel free to email me if you want to contribute your HTML/css files.

This application is currently being developed so that the following features are supported.

I am planning on initial release in September or October 2016.

My mother tongue is Korean, so the commit message will be written in Korean until the first official release.

## Features

* Blog
    * Search
    * Revision History and Status
    * Weighted Tags, Categories
    * Recent Posts, Recent Comments, Monthly Archives, Feeds
    * WYSIWYG editor and Markdown
    * Role-based Access Control
    * Attachment management
    * Social Share
    * Widgets
* Cart
    * Products, Brands, Vendors, Customers
* Authentication with strong password policy
* Role-based Access Control
* Custom config file support
    * ```test.cfg``` is provided, but you **must** have your own settings.
* Scalable structure with blueprint
    * templates and static folders
    * theme supported
* Fancy Frontend and Admin interface with AlloyUI 3 support
    * Bootstrap 3
    * YUI 3
* i18n / l10n support
* Unit Test
* Logging support
* MIT License

## Requirements

Rabiang is based on Flask/Python3, and it requires the following packages:

* **Flask**
* **Flask-SQLAlchemy** with **SQLAlchemy**
* **Flask-WTP** with **WTForms**
* **Flask-Babel** with **Babel** and **pytz**
* **Flask-Login**
* **Flask-Markdown** with **Markdown**, **Pygments** and **Bleach**
