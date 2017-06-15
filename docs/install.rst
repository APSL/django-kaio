Installation
============

To install the package

.. code-block:: python

    pip install django-kaio

Then you've to append :code:`kaio`  to :code:`INSTALLED_APPS` in your settings.

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'kaio',
    )


Configuration with django-configurations
----------------------------------------


To use class based settings, we need to configure django-configurations.
It's all explained here_.

.. _here: http://django-configurations.readthedocs.org/en/latest/


.. _config wsgi.py and manage.py:

Modifiying wsgi.py and manage.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We need to configure two files of our project: ``manage.py`` and ``wsgi.py``

* manage.py

.. code-block:: python

    #!/usr/bin/env python

    import os
    import sys

    if __name__ == "__main__":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
        os.environ.setdefault('DJANGO_CONFIGURATION', 'Base')

        from configurations.management import execute_from_command_line

        execute_from_command_line(sys.argv)


* wsgi.py

.. code-block:: python

    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Base')

    from configurations.wsgi import get_wsgi_application

    application = get_wsgi_application()

