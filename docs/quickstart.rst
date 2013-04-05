===========
Quick Start
===========

To quickly get started with **matchpoint**, clone this repository and
follow the steps below.


Requirements
============

You will need:

* Python, recommended 2.7.
* MongoDB_, 2.0 or higher.
* git

Recommended:

* virtualenv_
* pip_


Running the Server
==================

The included MongoDB config file does not fork by default. You will need
two terminals or to add the ``--fork`` option.

Start MongoDB::

    mongod --config=configs/mongod.dev.conf

Start Flask::

    python -m matchpoint

By default, the server will now be running on port 5000.

.. _MongoDB: http://www.mongodb.org/
.. _virtualenv: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org/
