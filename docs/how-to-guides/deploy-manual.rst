.. SPDX-FileCopyrightText: 2023 peepo.world developers
..
.. SPDX-License-Identifier: EUPL-1.2

.. _how-to-guides-deploy-manual:

*************
Manual deploy
*************

Pre-requirements
================

The web application requires the following services to run, so you must
configure them before starting it.


Database
--------

We use GINO_ for the database connection, you can use any of database backends
supported by it.


.. admonition:: Database backends supported by GINO_
   :class: hint

   At the time of writing, GINO_ supports PostgreSQL_ and MySQL_.


After you setup the database, you should set the ``DB_URL`` environment
variable according to your database setup.


.. code-block:: console
   :caption: ``bash`` command to set ``DB_URL``

   $ export DB_URL='postgresql://username:password@host:port/database'


.. admonition:: Configuring the Web-app
   :class: seealso

   You can find all the supported configuration settings in the
   :ref:`reference-config` page.


Object storage service
----------------------

.. todo::

   This isn't implemented yet, so it's not needed to run the web-app at the
   moment.


Spawning the app
================

``greenhouse`` exposes a ASGI_ app on the ``greenhouse.web.asgi`` module. You
can use any ASGI_ server implementation to run the app, but we recommend using
Gunicorn_ with the Uvicorn_ runner.


.. code-block:: console
   :caption: Spawn the ``greenhouse`` app with 4 workers

   $ gunicorn example:app -w 4 -k uvicorn.workers.UvicornWorker


.. _GINO: https://github.com/python-gino/gino
.. _PostgreSQL: https://www.postgresql.org/
.. _MySQL: https://www.mysql.com/
.. _ASGI: https://asgi.readthedocs.io/en/latest/
.. _Gunicorn: https://gunicorn.org/
.. _Uvicorn: https://www.uvicorn.org/
