.. _usage:

pymesync - Communicate with a TimeSync API
==========================================

This module provides an interface to communicate with an implementation of the
`OSU Open Source Lab`_'s `TimeSync`_ API. An example implementation in Node.js
can be found `on Github`_.

This module allows users to send times to TimeSync (**send_time()**), get a time
or a list of times from TimeSync (**get_times()**), and get a project or list of
projects from TimeSync (**get_projects()**).

Pymesync currently supports the following TimeSync API versions:

* v1

All of these methods return a python list of one to many dictionaries.

* **send_time(parameter_dict)** - Sends time to baseurl set in constructor
* **get_times([kwargs])** - Get times from TimeSync
* **get_projects([kwargs])** - Get project information from TimeSync

.. _OSU Open Source Lab: http://www.osuosl.org
.. _TimeSync: http://timesync.readthedocs.org/en/latest/
.. _on Github: https://github.com/osuosl/timesync-node

Install pymesync
----------------

Future implementation will allow you to simply ``pip install pymesync``, but for
now you need to copy the pymesync `source code`_ into your project and
``pip install -r requirements.txt`` in a virtualenv.

.. _source code: https://github.com/osuosl/pymesync

Initiate a TimeSync object:
---------------------------

To access pymesync's public methods you must first initiate a TimeSync object

.. code-block:: python

    import pymesync

    ts = pymesync.TimeSync(baseurl, user, password, auth_type)

Where

* ``baseurl`` is a string containing the url of the TimeSync instance you will
  communicate with. This must include the version endpoint (example
  ``"http://ts.example.com/v1"``)
* ``user`` is a string containing the username of the user communicating with
  TimeSync
* ``password`` is a string containing the user's password
* ``auth_type`` is a string containing the type of authentication your TimeSync
  implementation uses, such as ``"password"``, ``"ldap"``, or ``"token"``.

.. warning::

    ``"token"`` auth is not currently supported by pymesync


Public methods:
---------------

TimeSync.\ **send_time(parameter_dict)**

    Send a time entry to TimeSync via a POST request in a JSON body. This method
    will return that body in the form of a list containing a single python
    dictionary. The dictionary will contain a representation of that JSON body
    if it was successful or error information if it was not.

    ``parameter_dict`` is a python dictionary containing the time information to
    send to TimeSync.

TimeSync.\ **get_times([\**kwargs])**

    Request time entries filtered by parameters passed to ``kwargs``. Returns a
    list of python objects representing the JSON time information returned by
    TimeSync or an error message if unsuccessful.

    ``kwargs`` contains the optional query parameters described in the
    `TimeSync documentation`_. If ``kwargs`` is empty, ``get_times()`` will
    return all times in the database. The syntax for each argument is
    ``query=["parameter"]``.

    Currently the valid queries allowed by pymesync are:

    * ``user`` filter time request by user
    * ``project`` filter time request by project
    * ``activity`` filter time request by activity
    * ``start`` filter time request by start date
    * ``end`` filter time request by end date
    * ``revisions`` either ``["true"]`` or ``["false"]`` to include revisions of
      times

    .. _TimeSync documentation: http://timesync.readthedocs.org/en/latest/draft_api.html#get-endpoints

TimeSync.\ **get_projects([\**kwargs])**

    Request project information filtered by parameters passed to ``kwargs``.
    Returns a list of python objects representing the JSON project information
    returned by TimeSync or an error message if unsuccessful.

    ``kwargs`` contains the optional query parameters described in the
    `TimeSync documentation`_. If ``kwargs`` is empty, ``get_projects()`` will
    return all projects in the database. The syntax for each argument is
    ``query="parameter"`` or ``bool_query=<boolean>``.

    The optional parameters currently supported by the TimeSync API are:

    * ``slug`` filter project request by project slug

      - example: ``slug='gwm'``

    * ``include_deleted`` tell TimeSync whether to include deleted projects in
      request. Default is ``False``

      - example: ``include_deleted=True``

    * ``revisions`` tell TimeSync whether to include past revisions of projects
      in request. Default is ``False``

      - example: ``revisions=True``

    .. warning::

      Does not accept a ``slug`` combined with ``include_deleted``, but does
      accept any other combination.

Example usage:

.. code-block:: python

    >>> import pymesync
    >>>
    >>> ts = pymesync.TimeSync('http://ts.example.com/v1', 'username', 'userpass', 'password')
    >>> params = {
    ...             "duration": 12,
    ...             "project": "ganeti-web-manager",
    ...             "user": "example-user",
    ...             "activities": ["documenting"],
    ...             "notes": "Worked on docs",
    ...             "issue_uri": "https://github.com/",
    ...             "date_worked": 2014-04-17,
    ...         }
    >>> ts.send_times(params)
    {u'object': {u'activities': [u'documenting'], u'date_worked': 1993, u'notes': u'Worked on docs', u'project': u'ganeti-web-manager', u'user': u'example-user', u'duration': 12, u'issue_uri': u'https://github.com/', u'id': 1}, u'auth': {u'username': u'example-user', u'password': u'password', u'type': u'password'}}
    >>>
    >>> ts.get_times(user=["username"])
    {u'object': {u'activities': [u'documenting'], u'date_worked': 1993, u'notes': u'Worked on docs', u'project': u'ganeti-web-manager', u'user': u'example-user', u'duration': 12, u'issue_uri': u'https://github.com/', u'id': 1}, u'auth': {u'username': u'example-user', u'password': u'password', u'type': u'password'}}
    >>>
    >>> ts.get_projects(slug='gwm')
    {u'owner': u'example-user', u'slugs': [u'ganeti', u'gwm'], u'id': 1, u'uri': u'https://code.osuosl.org/projects/ganeti-webmgr', u'name': u'Ganeti Web Manager'}
