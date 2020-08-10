Django Views — The Right Way — code
===================================

This folder contains an app with code to accompany the guide. It's main purpose
is to make sure that the guide isn't buggy, but it can also serve as extra
explanation or illustration of things in the guide.

Structure
---------

Each page of the guide has a module defined inside ``the_right_way`` e.g.
``the_right_way.the_pattern``, which has ``views.py`` and ``urls.py`` defined in
it. There are some common models defined in ``shop``.


Running the app
---------------

::

   ./manage.py runserver

Browse at http://localhost:8000/ and http://localhost:8000/admin/


Other info
----------

A SQLite DB is included, with some minimal data in it.

There is a superuser with username ``admin`` and password ``admin``.
