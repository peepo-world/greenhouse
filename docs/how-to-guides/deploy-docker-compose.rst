.. SPDX-FileCopyrightText: 2023 peepo.world developers
..
.. SPDX-License-Identifier: EUPL-1.2

.. _how-to-guides-deploy-docker-compose:

*******************************
Deploying via `Docker Compose`_
*******************************

We provide a `Docker Compose`_ configuration in our repository_.


.. code-block:: console

   $ git clone https://github.com/peepo-world/greenhouse.git
   $ cd greenhouse


To quickly setup the app, you can use our `Docker Compose`_ configuration.

.. code-block:: console

   $ docker compose -f docker-compose/db.yml -f docker-compose/web.yml up


.. _Docker Compose: https://docs.docker.com/compose/
.. _repository: https://github.com/peepo-world/greenhouse
