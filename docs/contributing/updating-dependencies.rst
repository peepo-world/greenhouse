.. SPDX-FileCopyrightText: 2023 peepo.world developers
..
.. SPDX-License-Identifier: EUPL-1.2

.. _contributing-updating-dependencies:

*********************
Updating dependencies
*********************

We ship a lock file, ``requirements.txt``, with the recommend dependency
versions. The project is tested against this set of dependencies, so users are
recommended to use them to avoid breakage from newer dependency versions.

To update the ``requirements.txt``, we run the ``pip-compile`` command from the
`pip-tools`_ project, as follows:


.. code-block:: console

   $ pip-compile --extra=serve pyproject.toml


.. _pip-tools: https://github.com/jazzband/pip-tools
