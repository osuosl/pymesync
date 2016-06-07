pymesync
========

.. image:: https://travis-ci.org/osuosl/pymesync.svg?branch=master
    :target: https://travis-ci.org/osuosl/pymesync

Python module for TimeSync. Compatible with Python versions 2.7 and 3.3+

Pymesync documentation can be found on `readthedocs`_

We use virtualenv for development and testing:

.. code-block::

  $ virtualenv venv
  $ source venv/bin/activate
  (venv) $ pip install -r requirements.txt

For usage documentation, build our docs:

.. code-block::

  (venv) $ cd docs
  (venv) $ make html
  (venv) $ <browser> build/html/index.html

To test the source code:

.. code-block::

  (venv) $ make test
  (venv) $ make flake

or

.. code-block::

  (venv) $ make verify

.. _readthedocs: http://pymesync.readthedocs.org/en/latest/
