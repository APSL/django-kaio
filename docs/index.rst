.. django-kaio documentation master file, created by
   sphinx-quickstart on Tue Jun 13 12:57:40 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-kaio's documentation!
=======================================

**Django-kaio** is a django-package that helps us to configure our django project.
The values of the configuration can come from an .ini file or from environment settings.

The values are casted automatically, first trying to cast to *int*, then to *bool* and finally to *string*.

Also note that we can create class-based configurations settings, as django-configurations_ do.

.. _django-configurations: https://django-configurations.readthedocs.io/en/stable/#


Also includes:

* if the .ini file does not exist set the default values
* searches the .ini file in the current and parent directories
* managanement script to let us see the current project configuration
* management script to generate the .ini file with the default values
* uses django-configurations in order to be able to create class based settings
* mixins for standard configurations, such as Paths, Filer, Cache, Database...


.. toctree::
   install
   how_it_works
   management
   mixins
   example
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. todolist::

