pymesync
========

Python module for TimeSync

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
  (venv) $ make flake    # Runs flake8 on pymesync.py and tests.py

or

.. code-block::

  (venv) $ make verify   # Runs tests and flake8
