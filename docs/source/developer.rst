.. _developer:

Developer Documentation for Pymesync
====================================

Introduction
------------

When developing for pymesync, there are several things that need to be
considered, including communication with TimeSync, return formats, error
messages, testing, internal vs. external methods, test mode, and documenting
changes.

.. contents::

Communicating with TimeSync
---------------------------

Pymesync communicates with a user-defined TimeSync implementation using the
Python `requests`_ library. All POST requests to TimeSync must be in proper JSON
by passing the data to the `json variable`_ in the POST request.

TimeSync returns either a single JSON object or a list of several JSON objects.
These must be converted to a python dictionary or list of dictionary as
described in the next section.

.. _requests: http://docs.python-requests.org/en/latest/
.. _json variable: http://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests

Return Format
-------------

Pymesync usually returns a dictionary or a list of zero or more python
dictionaries (in the case of get methods). The return format is decided by the
information that will be returned by TimeSync. If TimeSync could return
multiple objects, Pymesync returns the dicts in a list, even if zero or one
object is returned.

Following this format, the user can use the same logic and syntax to process a
``get_<endpoint>()`` method that returns one object as they do for a
``get_<endpoint>()`` method that returns many objects. This is important because
filtering parameters can be passed to those methods that will get an unknown
number of objects from TimeSync.

The exception to this rule is for simple data returns like
``token_expiration_time()``, which returns a python datetime. 

Error Messages
--------------

Local pymesync error messages and TimeSync error messages returned from the API
should be returned in the same format as their parent method. Simple data
returns such as ``token_expiration_time()`` should return a python dictionary.

The key for the error message is set as a class variable in the
``pymesync.TimeSync`` class constructor. This class variable is called
``error`` and sets the key name throughout the module, including in the tests.
The value stored at the key location must be descriptive enough to help the
user debug their issue.

The TimeSync API also returns its own errors in a different format, like so:

.. code-block:: python

  [{"status": 401, "error": "Authentication failure", "text": "Invalid username or password"}]

Testing
-------

Pymesync makes some very expensive API calls to the TimeSync API. These calls
can tie up TimeSync resources or even change the state of the TimeSync database.

To test any method that makes an API call or uses an external resource, you
should mock it. Mocking in python involves a somewhat steep learning curve.
Read the `official documentation`_ and review the current pymesync tests that
rely on mocking to familiarize yourself.

.. _official documentation: https://docs.python.org/3/library/unittest.mock.html

External and Internal Methods
-----------------------------

There are several methods in pymesync that are available to the user, such as
``get_times()``, ``create_times()``, ``update_activity()``. Some are only usable
by an authenticated TimeSync administrator, but all are public. Write these
methods as you would write any other.

Several public methods accomplish very similar tasks and use an
`internal method`_ to keep the code `DRY`_. The trick is that in Python, there
aren't really any *truly* private methods. We prefix a method name with ``__``
(double underscore) to indicate that it is private. Python then "name mangles"
the method name to prevent name collisions with another class (again, see the
`documentation`_)

The result of the name mangling for a developer writing internal functions is in
the testing phase. When accessed externally, the ``__internal()`` method of the
``TimeSync`` class is renamed like the following:

.. code-block:: python

  ts_object._TimeSync__internal()

By using the mangled name, you can unit test the internal method.

.. _internal method: https://docs.python.org/2/tutorial/classes.html#tut-private
.. _DRY: https://en.wikipedia.org/wiki/Don%27t_repeat_yourself
.. _documentation: https://docs.python.org/2/tutorial/classes.html#tut-private

Test Mode
---------

Pymesync provides a :ref:`testing` mode so users can test their code without
having to mock pymesync. It just returns what the TimeSync API says it should
return on proper inputs.

If you write a new public method for pymesync, make sure you add it to the
``mock_pymesync.py`` file with a proper return. In the method you write,
include this logic so the test mode method is called instead when test mode is
on:

.. code-block:: python

  if self.test:
      return # your test mode method

Make sure you are returning your test mode method *after* all error checking is
complete.

Documenting Changes
-------------------

When you add a public method, please document it in the usage docs and the test
mode docs. Follow the format for already-existing methods.
