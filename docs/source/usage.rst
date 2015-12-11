.. _usage:

pymesync - Communicate with a TimeSync API
==========================================

.. contents::

This module provides an interface to communicate with an implementation of the
`OSU Open Source Lab`_'s `TimeSync`_ API. An example implementation in Node.js
can be found `on Github`_.

This module allows users to

* Send times, projects, and activities to TimeSync (**create_time()**,
  **create_project()**, **create_activity()**),
* Update times, projects, and activities (**update_time()**,
  **create_project()**, **update_activity()**)
* Get one or a list of times projects, and activities (**get_times()**,
  **get_projects()**, **get_activities()**)

Pymesync currently supports the following TimeSync API versions:

* v1

All of these methods return a list of one or more python dictionaries (or an
empty list if TimeSync has no records).

* **create_time(parameter_dict)** - Sends time to TimeSync baseurl set in
  constructor
* **create_project(parameter_dict)** - Send new project to TimeSync
* **create_activity(parameter_dict)** - Send new activity to TimeSync

|

* **update_time(parameter_dict, uuid)** - Update time entry specified by uuid
* **update_project(parameter_dict, slug)** - Update project specified by slug
* **update_activity(parameter_dict, slug)** - Update activity specified by slug

|

* **get_times(\**kwargs)** - Get times from TimeSync
* **get_projects(\**kwargs)** - Get project information from TimeSync
* **get_activities(\**kwargs)** - Get activity information from TimeSync

.. _OSU Open Source Lab: http://www.osuosl.org
.. _TimeSync: http://timesync.readthedocs.org/en/latest/
.. _on Github: https://github.com/osuosl/timesync-node

Install pymesync
----------------

Future implementation will allow you to simply ``pip install pymesync``, but for
now you need to copy or clone the pymesync `source code`_ into your project and
``pip install -r requirements.txt`` in a virtualenv.

.. _source code: https://github.com/osuosl/pymesync

Initiate a TimeSync object
--------------------------

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


Public methods
--------------

These methods are available to general TimeSync users with applicable user roles
on the projects they are submitting times to.

TimeSync.\ **create_time(parameter_dict)**

    Send a time entry to the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a list with
    a single python dictionary containing the created entry if successful. The
    dictionary will contain error information if ``create_time()`` was
    unsuccessful.

    ``parameter_dict`` is a python dictionary containing the time information to
    send to TimeSync. The syntax is ``"string_key": "string_value"`` with the
    exception of the key ``"duration"`` which takes an integer value, and the
    key ``"activities"``, which takes a list of strings containing activity
    slugs. ``create_time()`` accepts the following fields in ``parameter dict``:

    Required:

    * ``"duration"`` - duration of time spent working on project in seconds (per
      TimeSync API)
    * ``"project"`` - slug of project worked on
    * ``"user"`` - username of user that did the work, must match ``user``
      specified in instantiation
    * ``"activities"`` - list of slugs identifying the activies worked on for
      this time entry
    * ``"date_worked"`` - date worked for this time entry in the form
      ``"yyyy-mm-dd"``

    Optional:

    * ``"notes"`` - optional notes about this time entry
    * ``"issue_uri"`` - optional uri to issue worked on

    Example ``parameter_dict``:

    .. code-block:: python

      params = {
          "duration": 7200,
          "project": "ganeti-web-manager",
          "user": "example-user",
          "activities": ["documenting"],
          "notes": "Worked on docs",
          "issue_uri": "https://github.com/",
          "date_worked": "2014-04-17",
      }

------------------------------------------

TimeSync.\ **update_time(parameter_dict, uuid)**

    Update a time entry by uuid on the TimeSync instance specified by the
    baseurl provided when instantiating the TimeSync object. This method will
    return a list with a single python dictionary containing the updated entry
    if successful. The dictionary will contain error information if
    ``update_time()`` was unsuccessful.

    ``parameter_dict`` is a python dictionary containing the time information to
    send to TimeSync. The syntax is ``"string_key": "string_value"`` with the
    exception of the key ``"duration"`` which takes an integer value, and the
    key ``"activities"``, which takes a list of strings containing activity
    slugs. You only need to send the fields that you want to update.

    ``uuid`` is a string containing the uuid of the time to be updated.

    ``update_time()`` accepts the following fields in ``parameter dict``:

    * ``"duration"`` - duration of time spent working on project in seconds (per
      TimeSync API)
    * ``"project"`` - slug of project worked on
    * ``"user"`` - username of user that did the work, must match ``user``
      specified in instantiation
    * ``"activities"`` - list of slugs identifying the activies worked on for
      this time entry
    * ``"date_worked"`` - date worked for this time entry in the form
      ``"yyyy-mm-dd"``
    * ``"notes"`` - optional notes about this time entry
    * ``"issue_uri"`` - optional uri to issue worked on

    Example ``parameter_dict`` to update the date_worked of a time entry:

    .. code-block:: python

      params = {
          "date_worked": "2015-04-17",
      }

------------------------------------------

TimeSync.\ **get_times(\**kwargs)**

    Request time entries from the TimeSync instance specified by the baseurl
    provided when instantiating the TimeSync object. The time entries are
    filtered by parameters passed to ``kwargs``. Returns a list of python
    dictionaries containing the time information returned by TimeSync or an
    error message if unsuccessful.

    ``kwargs`` contains the optional query parameters described in the
    `TimeSync documentation`_. If ``kwargs`` is empty, ``get_times()`` will
    return all times in the database. The syntax for each argument is
    ``query=["parameter1", "parameter2"]`` except for the ``id`` parameter which
    is ``id=<integer-id>``.

    Currently the valid queries allowed by pymesync are:

    * ``user`` - filter time request by username

      - example: ``user=["username"]``

    * ``project`` - filter time request by project slug

      - example: ``project=["slug"]``

    * ``activity`` - filter time request by activity slug

      - example: ``activity=["slug"]``

    * ``start`` - filter time request by start date

      - example: ``start=["2014-07-23"]``

    * ``end`` - filter time request by end date

      - example: ``end=["2015-07-23"]``

    * ``revisions`` - either ``["true"]`` or ``["false"]`` to include revisions
      of times

      - example: ``revisions=["true"]``

    * ``id`` - get specific time entry by time id

      - example: ``id=134``

    .. warning::

      If the ``id`` parameter is passed all other parameters will be ignored.
      For example, ``ts.get_times(id=12, user=["bob"])`` is equivalent to
      ``ts.get_times(id=12)``.

------------------------------------------

TimeSync.\ **get_projects(\**kwargs)**

    Request project entries from the TimeSync instance specified by the baseurl
    provided when instantiating the TimeSync object. The project entries are
    filtered by parameters passed to ``kwargs``. Returns a list of python
    dictionaries containing the project information returned by TimeSync or an
    error message if unsuccessful.

    ``kwargs`` contains the optional query parameters described in the
    `TimeSync documentation`_. If ``kwargs`` is empty, ``get_projects()`` will
    return all projects in the database. The syntax for each argument is
    ``query="parameter"`` or ``bool_query=<boolean>``.

    The optional parameters currently supported by the TimeSync API are:

    * ``slug`` - filter project request by project slug

      - example: ``slug='gwm'``

    * ``include_deleted`` - tell TimeSync whether to include deleted projects in
      request. Default is ``False`` and cannot be combined with a ``slug``.

      - example: ``include_deleted=True``

    * ``revisions`` - tell TimeSync whether to include past revisions of
      projects in request. Default is ``False``

      - example: ``revisions=True``

    .. warning::

      Does not accept a ``slug`` combined with ``include_deleted``, but does
      accept any other combination.

------------------------------------------

TimeSync.\ **get_activities(\**kwargs)**

    Request activity entries from the TimeSync instance specified by the baseurl
    provided when instantiating the TimeSync object. The activity entries are
    filtered by parameters passed to ``kwargs``. Returns a list of python
    dictionaries containing the activity information returned by TimeSync or an
    error message if unsuccessful.

    ``kwargs`` contains the optional query parameters described in the
    `TimeSync documentation`_. If ``kwargs`` is empty, ``get_activities()`` will
    return all activities in the database. The syntax for each argument is
    ``query="parameter"`` or ``bool_query=<boolean>``.

    The optional parameters currently supported by the TimeSync API are:

    * ``slug`` - filter activity request by activity slug

      - example: ``slug='code'``

    * ``include_deleted`` - tell TimeSync whether to include deleted activities
      in request. Default is ``False`` and cannot be combined with a ``slug``.

      - example: ``include_deleted=True``

    * ``revisions`` - tell TimeSync whether to include past revisions of
      activities in request. Default is ``False``

      - example: ``revisions=True``

    .. warning::

      Does not accept a ``slug`` combined with ``include_deleted``, but does
      accept any other combination.

------------------------------------------

.. _TimeSync documentation: http://timesync.readthedocs.org/en/latest/draft_api.html#get-endpoints

Administrative methods
----------------------

These methods are available to TimeSync users with administrative permissions.

TimeSync.\ **create_project(parameter_dict)**

    Create a project on the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a list with
    a single python dictionary containing the created project if successful. The
    dictionary will contain error information if ``create_project()`` was
    unsuccessful.

    ``parameter_dict`` is a python dictionary containing the project
    information to send to TimeSync. The syntax is ``"key": "value"`` except for
    the ``"slugs"`` field, which is ``"slugs": ["slug1", "slug2", "slug3"]``.
    ``parameter_dict`` requires the following fields:

    * ``"uri"``
    * ``"name"``
    * ``"slugs"`` - this must be a list of strings
    * ``"owner"``

    Example ``parameter_dict``:

    .. code-block:: python

      parameter_dict = {
          "uri": "https://code.osuosl.org/projects/timesync",
          "name": "TimeSync API",
          "slugs": ["timesync", "time"],
          "owner": "mrsj"
      }

------------------------------------------

TimeSync.\ **update_project(parameter_dict, slug)**

    Update an existing project by slug on the TimeSync instance specified by the
    baseurl provided when instantiating the TimeSync object. This method will
    return a list with a single python dictionary containing the updated project
    if successful. The dictionary will contain error information if
    ``update_project()`` was unsuccessful.

    ``parameter_dict`` is a python dictionary containing the project
    information to send to TimeSync. The syntax is ``"key": "value"`` except for
    the ``"slugs"`` field, which is ``"slugs": ["slug1", "slug2", "slug3"]``.

    ``slug`` is a string containing the slug of the project to be updated.

    If ``"uri"``, ``"name"``, or ``"owner"`` are set to ``""`` (empty string) or
    ``"slugs"`` is set to ``[]`` (empty array), the value will be set to the
    empty string/array.

    You only need to pass the fields you want to update in ``parameter_dict``.

    ``parameter_dict`` accepts the following fields:

    * ``"uri"``
    * ``"name"``
    * ``"slugs"`` - this must be a list of strings
    * ``"owner"``

    Example ``parameter_dict`` to update project slugs:

    .. code-block:: python

      parameter_dict = {
          "slugs": ["timesync", "time", "ts"]
      }

------------------------------------------

TimeSync.\ **create_activity(parameter_dict)**

    Create an activity on the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a list with
    a single python dictionary containing the created activity if successful.
    The dictionary will contain error information if ``create_activity()`` was
    unsuccessful.

    ``parameter_dict`` is a python dictionary containing the activity
    information to send to TimeSync. The syntax is ``"key": "value"``.
    ``parameter_dict`` requires the following fields:

    * ``"name"``
    * ``"slug"``

    Example ``parameter_dict``:

    .. code-block:: python

      parameter_dict = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
      }

------------------------------------------

TimeSync.\ **update_activity(parameter_dict, slug)**

    Update an existing activity by slug on the TimeSync instance specified by
    the baseurl provided when instantiating the TimeSync object. This method
    will return a list with a single python dictionary containing the updated
    activity if successful. The dictionary will contain error information if
    ``update_activity()`` was unsuccessful.

    ``parameter_dict`` is a python dictionary containing the project
    information to send to TimeSync. The syntax is ``"key": "value"``.

    ``slug`` is a string containing the slug of the activity to be updated.

    If ``"name"`` or ``"slug"`` in ``parameter_dict`` are set to ``""``
    (empty string), the value will be set to the empty string.

    You only need to pass the fields you want to update in ``parameter_dict``.

    ``parameter_dict`` accepts the following fields to update an activity:

    * ``"name"``
    * ``"slug"``

    Example ``parameter_dict`` to update activity slug:

    .. code-block:: python

      parameter_dict = {
            "slug": "test"
      }

------------------------------------------



Example usage
-------------

.. code-block:: python

    >>> import pymesync
    >>>
    >>> ts = pymesync.TimeSync('http://ts.example.com/v1', 'username', 'userpass', 'password')
    >>> params = {
    ...    "duration": 12,
    ...    "project": "ganeti-web-manager",
    ...    "user": "username",
    ...    "activities": ["documenting"],
    ...    "notes": "Worked on docs",
    ...    "issue_uri": "https://github.com/",
    ...    "date_worked": "2014-04-17",
    ...}
    >>> ts.create_time(params)
    [{u'object': {u'activities': [u'documenting'], u'date_worked': u'2014-04-17', u'notes': u'Worked on docs', u'project': u'ganeti-web-manager', u'user': u'username', u'duration': 12, u'issue_uri': u'https://github.com/', u'id': 1}, u'auth': {u'username': u'username', u'password': u'userpass', u'type': u'password'}}]
    >>> ts.get_times(user=["username"])
    [{u'object': {u'activities': [u'documenting'], u'date_worked': u'2014-04-17', u'notes': u'Worked on docs', u'project': u'ganeti-web-manager', u'user': u'username', u'duration': 12, u'issue_uri': u'https://github.com/', u'id': 1}, u'auth': {u'username': u'username', u'password': u'userpass', u'type': u'password'}}]
    >>> ts.get_projects(slug='gwm')
    [{u'owner': u'username', u'slugs': [u'ganeti', u'gwm'], u'id': 1, u'uri': u'https://code.osuosl.org/projects/ganeti-webmgr', u'name': u'Ganeti Web Manager'}]
    >>> ts.get_activities(slug='code')
    [{"id":1,"name":"Programming","slug":"code","created_at":"2015-11-24","updated_at":null,"deleted_at":null,"uuid":"fd7fd535-1272-44cd-b4ec-726b65b1db96","revision":1}]
    >>> project_params = {
    ...    "uri": "https://code.osuosl.org/projects/timesync",
    ...    "name": "TimeSync API",
    ...    "slugs": ["timesync", "time"],
    ...    "owner": "username"
    ...}
    >>> ts.create_project(project_params)
    [{u'uuid': u'someuuid', u'created_at': u'2015-11-24', u'uri': u'https://code.osuosl.org/projects/timesync', u'id': 2, u'owner': u'username', u'revision': 1, u'slugs': [u'timesync', u'time'], u'name': u'TimeSync API'}]
    >>>
