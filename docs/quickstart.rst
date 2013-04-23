.. _quickstart-chatper:

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

* virtualenv_ and virtualenvwrapper_.
* pip_


Installing
==========

::

    git clone git://github.com/jsocol/matchpoint.git
    cd matchpoint
    mkvirtualenv matchpoint
    pip install -r requirements.txt


Running the Server
==================

The included MongoDB config file does not fork by default. You will need
two terminals or to add the ``--fork`` option.

Start MongoDB::

    mongod --config=configs/mongod.dev.conf

Start Flask::

    python app.py

By default, the server will now be running on port 5000.


Entering Data
=============

To get data into the server right now the easiest method is via a Python
shell.

::

    >>> from datetime import datetime
    >>> from matchpoint.models import *
    >>> myns = Namespace()
    >>> myns.name = 'mozilla-en_US'
    >>> myns.modified = datetime.now()
    >>> int = Interest()
    >>> int.name = 'cars'
    >>> int.modified = myns.modified
    >>> intver = InterestVersion()
    >>> intver.modified = myns.modified
    >>> intver.duration = 90
    >>> intver.threshold = 4
    >>> match = Match()
    >>> match.keywords = ['car', 'vehicle']
    >>> match.domains = ['toyota.com', 'ford.com']
    >>> intver.matches = [match]
    >>> int.current = intver
    >>> int.versions = [current]
    >>> myns.interests = [int]
    >>> myns.save()

To retrieve this data, you would make the following request::

    curl -i http://localhost:5000/api/v1/mozilla-en_US

You will see a ``Last-Modified`` header in the response.


.. _MongoDB: http://www.mongodb.org/
.. _virtualenv: http://www.virtualenv.org/
.. _virtualenvwrapper: https://pypi.python.org/pypi/virtualenvwrapper
.. _pip: http://www.pip-installer.org/
