Management scripts
==================

We have to management scripts available in order to see the current
configurations values and to generate a file with default values into the standard output.

apsettings
----------

We use it to see the current configurations values.

.. code-block:: python

    python manage.py apsettings

It shows the current configuration. In three columns:
* final values into the settings
* params into the .ini file
* param default value


generate_ini
------------

We use it to generate a file with default values into the standard output.

.. code-block:: python

    python manage.py generate_ini



