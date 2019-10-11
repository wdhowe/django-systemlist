===========
System List
===========

System List is a Django app to keep track of system inventory.
In order to add/modify system or OS types, see models.py.

Detailed documentation is in the "docs" directory.

Build package
-----------

Build the package by:

``python3 setup.py sdist``

Quick start
-----------

1. Add "systemlist" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'systemlist',
    ]

2. Include the systemlist URLconf in your project urls.py like this::

    path('systemlist/', include('systemlist.urls')),

3. Run `python manage.py migrate` to create the systemlist database models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create system list entries (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/systemlist/ to view the list and statistics.

