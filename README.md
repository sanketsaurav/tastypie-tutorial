Delicious RESTful APIs with Django Tastypie
===========================================
By [@sanketsaurav](http://twitter.com/sanketsaurav).

Tastypie is a webservice API framework for Django. It provides a convenient, yet powerful and highly customizable, abstraction for creating REST-style interfaces.


Agenda
------

- Brief introduction to RESTful API interfaces, CRUD, and why you should consider having an API

- Creating your first API

- Tastypie configuration and design features

- Understanding the lifetime of an API request

- Deeper look into ModelResource - general and relationship fields

- Authorization, Authentication and Caching

- Advanced data preparation

- Nested resources

- Testing


Requirements
------------

- Python v2.7.x. If you don't have it already, you can grab it [here](https://www.python.org/downloads/).

- SQLite. Any recent version would do.

- Your favorite text editor. Mine's [ST3](http://www.sublimetext.com/3).


Installation
------------

1. Clone this repository in your workspace.

```
git clone git@github.com:sanketsaurav/tastypie-tutorial.git
```

2. Install virtualenvwrapper. Instructions specific to your OS can be found [here](http://virtualenvwrapper.readthedocs.org/en/latest/install.html).

3. Create a new virtualenv, and install the requirements of this project.

```
cd tastypie-tutorial
pip install -r requirements.txt
```

4. Start your Django dev server.
```
python manage.py runserver
```

5. Follow along!