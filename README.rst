pymesync
========

Python module for TimeSync

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

  (venv) $ nosetests
  (venv) $ flake8 pymesync tests  # Runs flake8 on pymesync and tests

.. _readthedocs: http://pymesync.readthedocs.org/en/latest/
