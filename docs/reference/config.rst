.. SPDX-FileCopyrightText: 2023 peepo.world developers
..
.. SPDX-License-Identifier: EUPL-1.2

.. _reference-config:

*********************
Web-app Configuration
*********************

We starlette_'s ``config`` module for configuration, so you can configure the
app by setting environment variables for the configuration keys, or by creating
a ``.env`` in the current directory. Please refer to
`starlette's config documentation`_ for more information.

Configuration keys
==================

.. list-table::
   :widths: 15 85
   :header-rows: 1
   :stub-columns: 1

   * - Name
     - Description

   * - ``DEBUG``
     - Enables debug mode (defaults to ``false``).

       Please refer to `starlette's exceptions documentation`_ for more
       information.

   * - ``APP_HOST``
     - Sets the application host name (defaults to ``127.0.0.1``).

   * - ``APP_PORT``
     - Sets the application HTTP port name (defaults to ``8000``).

   * - ``APP_URL``
     - Sets the application URL (defaults to ``http://127.0.0.1:8000``).

   * - ``DB_URL``
     - Sets the database connection URL (defaults to
       ``postgresql://postgres:example@localhost/greenhouse``).

       Please refer to `SQLAlchemy's database URLs documentation`_ for more
       information.


.. _starlette: https://www.starlette.io/config/
.. _starlette's config documentation: https://www.starlette.io/config/
.. _starlette's exceptions documentation: https://www.starlette.io/exceptions/
.. _SQLAlchemy's database URLs documentation: https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
