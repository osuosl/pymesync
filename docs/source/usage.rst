.. _usage:

pymesync - Communicate with a TimeSync API
==========================================

.. contents::

This module provides an interface to communicate with an implementation of the
`OSU Open Source Lab`_'s `TimeSync API`_. An implementation of the TimeSync API,
built in Node.js, can be found at `github.com/osuosl/timesync-node`_.

This module allows users to

* Authenticate a pymesync object with a TimeSync implementation
  (**authenticate()**)
* Send times, projects, activities, and users to TimeSync (**create_time()**,
  **create_project()**, **create_activity()**, **create_user()**),
* Update times, projects, activities, and users (**update_time()**,
  **update_project()**, **update_activity()**, **update_user()**)
* Get one or a list of times projects, activities, and users (**get_times()**,
  **get_projects()**, **get_activities()**, **get_users()**)
* Delete an object in the TimeSync database (**delete_time()**,
  **delete_project()**, **delete_activity()**, **delete_user()**)

Pymesync currently supports the following TimeSync API versions:

* v1

All of these methods return a list of one or more python dictionaries (or an
empty list if TimeSync has no records).

* **authenticate(username, password, auth_type)** - Authenticates a pymesync
  object with a TimeSync implementation

|

* **create_time(time)** - Sends time to TimeSync baseurl set in
  constructor
* **create_project(project)** - Send new project to TimeSync
* **create_activity(activity)** - Send new activity to TimeSync
* **create_user(user)** - Send a new user to TimeSync

|

* **update_time(time, uuid)** - Update time entry specified by uuid
* **update_project(project, slug)** - Update project specified by slug
* **update_activity(activity, slug)** - Update activity specified by slug
* **update_user(user, username)** - Update user specified by username

|

* **get_times(\**kwargs)** - Get times from TimeSync
* **get_projects(\**kwargs)** - Get project information from TimeSync
* **get_activities(\**kwargs)** - Get activity information from TimeSync
* **get_users(username=None)** - Get user information from TimeSync

|

* **delete_time(uuid)** - Delete time entry from TimeSync
* **delete_project(slug)** - Delete project record from TimeSync
* **delete_activity(slug)** - Delete activity record from TimeSync
* **delete_user(username)** - Delete user record from TimeSync

.. _OSU Open Source Lab: http://www.osuosl.org
.. _TimeSync API: http://timesync.readthedocs.org/en/latest/
.. _github.com/osuosl/timesync-node: https://github.com/osuosl/timesync-node

Install pymesync
----------------

Future implementation will allow you to simply ``pip install pymesync``, but for
now you need to copy or clone the pymesync `source code`_ into your project and
``pip install -r requirements.txt`` in a virtualenv.

.. _source code: https://github.com/osuosl/pymesync

Initiate and Authenticate a TimeSync object
-------------------------------------------

To access pymesync's public methods you must first initiate a TimeSync object

.. code-block:: python

    import pymesync

    ts = pymesync.TimeSync(baseurl="http://ts.example.com/v1")
    ts.authenticate(username="user", password="password", auth_type="password")

Where

* ``baseurl`` is a string containing the url of the TimeSync instance you will
  communicate with. This must include the version endpoint (example
  ``"http://ts.example.com/v1"``)
* ``user`` is a string containing the username of the user communicating with
  TimeSync
* ``password`` is a string containing the user's password
* ``auth_type`` is a string containing the type of authentication your TimeSync
  implementation uses for login, such as ``"password"``, or ``"ldap"``.

You can also optionally include a token in the constructor like so:

.. code-block:: python

  import pymesync

  ts = pymesync.TimeSync(baseurl="http://ts.example.com/v1", token="SOMETOKENYOUGOTEARLIER")
  # ts.authenticate() is not required

This is handy when state is not kept between different parts of your system, but
you don't want to have to re-authenticate your TimeSync objectfor every section
of code.

.. note::

  If you attempt to get, create, or update objects before authenticating,
  pymesync will return this error:

  .. code-block:: python

    [{"pymesync error": "Not authenticated with TimeSync, call self.authenticate() first"}]

Errors
------

Pymesync returns errors the same way it returns all other information: as a
Python dictionary inside a list. If the error is a local pymesync error, the
key for the error message will be ``"pymesync error"``. If the error is from
TimeSync, the dictionary will contain the same keys described in the
`TimeSync error documentation`_, but as a python dictionary.

If there is an error connecting with the TimeSync instance specified by the
baseurl passed to the pymesync constructor, the error will also contain the
status code of the response. For example:

.. code-block:: python

    [{"pymesync error": "connection to TimeSync failed at baseurl http://ts.example.com/v1 - response status was 502"}]

.. _TimeSync error documentation: http://timesync.readthedocs.org/en/latest/draft_errors.html

Public methods
--------------

These methods are available to general TimeSync users with applicable user roles
on the projects they are submitting times to.

TimeSync.\ **authenticate(user, password, auth_type)**

    Authenticate a pymesync object with a TimeSync implementation. The
    authentication is subject to any time limits imposed by that implementation.

    ``user`` is a string containing the username of the user communicating with
    TimeSync

    ``password`` is a string containing the user's password

    ``auth_type`` is a string containing the type of authentication your
    TimeSync implementation uses for login, such as ``"password"``, or
    ``"ldap"``.

    **authenticate()** will return a list containing a python dictionary. If
    authentication was successful, the list will look like this:

    .. code-block:: python

      [{"token": "SOMELONGTOKEN"}]

    If authentication was unsuccessful, the list will contain an error message:

    .. code-block:: python

      [{"status": 401, "error": "Authentication failure", "text": "Invalid username or password"}]

    Example:

    .. code-block:: python

      >>> ts.authenticate(username="example-user", password="example-password", auth_type="password")
      [{u'token': u'eyJ0eXAi...XSnv0ghQ=='}]
      >>>

TimeSync.\ **token_expiration_time()**

    Returns a python datetime representing the expiration time of the current
    authentication token.

    Example:

    .. code-block:: python

      >>> ts.authenticate(username="username", password="user-pass", auth_type="password")
      [{u'token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJITUFDLVNIQTUxMiJ9.eyJpc3MiOiJvc3Vvc2wtdGltZXN5bmMtc3RhZ2luZyIsInN1YiI6InRlc3QiLCJleHAiOjE0NTI3MTQzMzQwODcsImlhdCI6MTQ1MjcxMjUzNDA4N30=.QP2FbiY3I6e2eN436hpdjoBFbW9NdrRUHbkJ+wr9GK9mMW7/oC/oKnutCwwzMCwjzEx6hlxnGo6/LiGyPBcm3w=='}]
      >>> ts.token_expiration_time()
      datetime.datetime(2016, 1, 13, 11, 45, 34)
      >>>

TimeSync.\ **create_time(time)**

    Send a time entry to the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a list with
    a single python dictionary containing the created entry if successful. The
    dictionary will contain error information if ``create_time()`` was
    unsuccessful.

    ``time`` is a python dictionary containing the time information to send to
    TimeSync. The syntax is ``"string_key": "string_value"`` with the exception
    of the key ``"duration"`` which takes an integer value, and the key
    ``"activities"``, which takes a list of strings containing activity slugs.
    ``create_time()`` accepts the following fields in ``time``:

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

    Example usage:

    .. code-block:: python

      >>> time = {
      ...    "duration": 1200,
      ...    "user": "example-2",
      ...    "project": "ganeti_web_manager",
      ...    "activities": ["docs"],
      ...    "notes": "Worked on documentation toward settings configuration.",
      ...    "issue_uri": "https://github.com/osuosl/ganeti_webmgr/issues",
      ...    "date_worked": "2014-04-17"
      ...}
      >>> ts.create_time(time=time)
      [{'activities': ['docs'], 'deleted_at': None, 'date_worked': '2014-04-17', 'uuid': '838853e3-3635-4076-a26f-7efr4e60981f', 'notes': 'Worked on documentation toward settings configuration.', 'updated_at': None, 'project': 'ganeti_web_manager', 'user': 'example-2', 'duration': 1200, 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr/issues', 'created_at': '2015-05-23', 'revision': 1}]
      >>>

------------------------------------------

TimeSync.\ **update_time(time, uuid)**

    Update a time entry by uuid on the TimeSync instance specified by the
    baseurl provided when instantiating the TimeSync object. This method will
    return a list with a single python dictionary containing the updated entry
    if successful. The dictionary will contain error information if
    ``update_time()`` was unsuccessful.

    ``time`` is a python dictionary containing the time information to send to
    TimeSync. The syntax is ``"string_key": "string_value"`` with the exception
    of the key ``"duration"`` which takes an integer value, and the key
    ``"activities"``, which takes a list of strings containing activity slugs.
    You only need to send the fields that you want to update.

    ``uuid`` is a string containing the uuid of the time to be updated.

    ``update_time()`` accepts the following fields in ``time``:

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

    Example usage:

    .. code-block:: python

      >>> time = {
      ...    "duration": 1900,
      ...    "user": "red-leader",
      ...    "activities": ["hello", "world"],
      ...}
      >>> ts.update_time(time=time, uuid="some-uuid")
      [{'activities': ['hello', 'world'], 'date_worked': '2015-08-07', 'updated_at': '2015-10-18', 'user': 'red-leader', 'duration': 1900, 'deleted_at': None, 'uuid': 'some-uuid', 'notes': None, 'project': ['ganeti'], 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr/issues/56', 'created_at': '2014-06-12', 'revision': 2}]

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
    ``query=["parameter1", "parameter2"]`` except for the ``uuid`` parameter
    which is ``uuid="uuid-as-string"`` and the ``include_deleted`` and
    ``include_revisions`` parameters which should be set to booleans.

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

    * ``include_revisions`` - either ``True`` or ``False`` to include
      revisions of times. Defaults to ``False``

      - example: ``include_revisions=True``

    * ``include_deleted`` - either ``True`` or ``False`` to include
      deleted times. Defaults to ``False``

      - example: ``include_deleted=True``

    * ``uuid`` - get specific time entry by time uuid

      - example: ``uuid="someuuid"``

      To get a deleted time by ``uuid``, also add the ``include_deleted``
      parameter.

    Example usage:

    .. code-block:: python

      >>> ts.get_times()
      [{'activities': ['docs', 'planning'], 'date_worked': '2014-04-17', 'updated_at': None, 'user': 'userone', 'duration': 1200, 'deleted_at': None, 'uuid': 'c3706e79-1c9a-4765-8d7f-89b4544cad56', 'notes': 'Worked on documentation.', 'project': ['ganeti-webmgr', 'gwm'], 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr', 'created_at': '2014-04-17', 'revision': 1}, {'activities': ['code', 'planning'], 'date_worked': '2014-04-17', 'updated_at': None, 'user': 'usertwo', 'duration': 1300, 'deleted_at': None, 'uuid': '12345676-1c9a-rrrr-bbbb-89b4544cad56', 'notes': 'Worked on coding', 'project': ['ganeti-webmgr', 'gwm'], 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr', 'created_at': '2014-04-17', 'revision': 1}, {'activities': ['code'], 'date_worked': '2014-04-17', 'updated_at': None, 'user': 'userthree', 'duration': 1400, 'deleted_at': None, 'uuid': '12345676-1c9a-ssss-cccc-89b4544cad56', 'notes': 'Worked on coding', 'project': ['timesync', 'ts'], 'issue_uri': 'https://github.com/osuosl/timesync', 'created_at': '2014-04-17', 'revision': 1}]
      >>>

    .. warning::

      If the ``uuid`` parameter is passed all other parameters will be ignored
      except for ``include_deleted`` and ``include_revisions``. For example,
      ``ts.get_times(uuid="time-entry-uuid", user=["bob"])`` is equivalent to
      ``ts.get_times(uuid="time-entry-uuid")``.

------------------------------------------

TimeSync.\ **delete_time(uuid)**

    Allows the currently authenticated user to delete their own time entry by
    uuid.

    ``uuid`` is a string containing the uuid of the time entry to be deleted.

    **delete_time()** returns a ``[{"status": 200}]`` if successful or an error
    message if unsuccessful.

    Example usage:

    .. code-block:: python

      >>> ts.delete_time(uuid="some-uuid")
      [{"status": 200}]
      >>>

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

    * ``include_revisions`` - tell TimeSync whether to include past revisions of
      projects in request. Default is ``False``

      - example: ``include_revisions=True``

    Example usage:

    .. code-block:: python

      >>> ts.get_projects()
      [{'users': {'managers': ['tschuy'], 'spectators': ['tschuy'], 'members': ['patcht', 'tschuy']}, 'uuid': 'a034806c-00db-4fe1-8de8-514575f31bfb', 'deleted_at': None, 'name': 'Ganeti Web Manager', 'updated_at': '2014-07-20', 'created_at': '2014-07-17', 'revision': 4, 'uri': 'https://code.osuosl.org/projects/ganeti-webmgr', 'slugs': ['gwm']}, {'users': {'managers': ['tschuy'], 'spectators': ['tschuy', 'mrsj'], 'members': ['patcht', 'tschuy', 'mrsj']}, 'uuid': 'a034806c-rrrr-bbbb-8de8-514575f31bfb', 'deleted_at': None, 'name': 'TimeSync', 'updated_at': '2014-07-20', 'created_at': '2014-07-17', 'revision': 2, 'uri': 'https://code.osuosl.org/projects/timesync', 'slugs': ['timesync', 'ts']}, {'users': {'managers': ['mrsj'], 'spectators': ['tschuy', 'mrsj'], 'members': ['patcht', 'tschuy', 'mrsj', 'MaraJade', 'thai']}, 'uuid': 'a034806c-ssss-cccc-8de8-514575f31bfb', 'deleted_at': None, 'name': 'pymesync', 'updated_at': '2014-07-20', 'created_at': '2014-07-17', 'revision': 1, 'uri': 'https://code.osuosl.org/projects/pymesync', 'slugs': ['pymesync', 'ps']}]
      >>>

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

    * ``include_revisions`` - tell TimeSync whether to include past revisions of
      activities in request. Default is ``False``

      - example: ``include_revisions=True``

    Example usage:

    .. code-block:: python

      >>> ts.get_activities()
      [{'uuid': 'adf036f5-3d49-4a84-bef9-062b46380bbf', 'created_at': '2014-04-17', 'updated_at': None, 'name': 'Documentation', 'deleted_at': None, 'slugs': ['docs'], 'revision': 5}, {'uuid': 'adf036f5-3d49-bbbb-rrrr-062b46380bbf', 'created_at': '2014-04-17', 'updated_at': None, 'name': 'Coding', 'deleted_at': None, 'slugs': ['code', 'dev'], 'revision': 1}, {'uuid': 'adf036f5-3d49-cccc-ssss-062b46380bbf', 'created_at': '2014-04-17', 'updated_at': None, 'name': 'Planning', 'deleted_at': None, 'slugs': ['plan', 'prep'], 'revision': 1}]
      >>>

    .. warning::

      Does not accept a ``slug`` combined with ``include_deleted``, but does
      accept any other combination.

------------------------------------------

TimeSync.\ **get_users(username=None)**

    Request user entities from the TimeSync instance specified by the baseurl
    provided when instantiating the TimeSync object. Returns a list of python
    dictionaries containing the user information returned by TimeSync or an
    error message if unsuccessful.

    ``username`` is an optional parameter containing a string of the specific
    username to be retrieved. If ``username`` is not provided, a list containing
    all users will be returned. Defaults to ``None``.

    Example usage:

    .. code-block:: python

      >>> ts.get_users()
      [{'username': 'userone', 'displayname': 'One Is The Loneliest Number', 'admin': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'exampleone@example.com'}, {'username': 'usertwo', 'displayname': 'Two Can Be As Bad As One', 'admin': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'exampletwo@example.com'}, {'username': 'userthree', 'displayname': "Yes It's The Saddest Experience", 'admin': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'examplethree@example.com'}, {'username': 'userfour', 'displayname': "You'll Ever Do", 'admin': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'examplefour@example.com'}]
      >>>

------------------------------------------

.. _TimeSync documentation: http://timesync.readthedocs.org/en/latest/draft_api.html#get-endpoints

Administrative methods
----------------------

These methods are available to TimeSync users with administrative permissions.

TimeSync.\ **create_project(project)**

    Create a project on the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a list with
    a single python dictionary containing the created project if successful. The
    dictionary will contain error information if ``create_project()`` was
    unsuccessful.

    ``project`` is a python dictionary containing the project information to
    send to TimeSync. The syntax is ``"key": "value"`` except for the
    ``"slugs"`` field, which is ``"slugs": ["slug1", "slug2", "slug3"]``.
    ``project`` requires the following fields:

    * ``"uri"``
    * ``"name"``
    * ``"slugs"`` - this must be a list of strings
    * ``"owner"``

    Example usage:

    .. code-block:: python

      >>> project = {
      ...    "uri": "https://code.osuosl.org/projects/timesync",
      ...    "name": "TimeSync API",
      ...    "slugs": ["timesync", "time"],
      ...}
      >>>
      >>> ts.create_project(project=project)
      [{'deleted_at': None, 'uuid': '309eae69-21dc-4538-9fdc-e6892a9c4dd4', 'updated_at': None, 'created_at': '2015-05-23', 'uri': 'https://code.osuosl.org/projects/timesync', 'name': 'TimeSync API', 'revision': 1, 'slugs': ['timesync', 'time'], 'users': {'managers': ['tschuy'], 'spectators': ['tschuy'], 'members': ['patcht', 'tschuy']}}]
      >>>

------------------------------------------

TimeSync.\ **update_project(project, slug)**

    Update an existing project by slug on the TimeSync instance specified by the
    baseurl provided when instantiating the TimeSync object. This method will
    return a list with a single python dictionary containing the updated project
    if successful. The dictionary will contain error information if
    ``update_project()`` was unsuccessful.

    ``project`` is a python dictionary containing the project information to
    send to TimeSync. The syntax is ``"key": "value"`` except for the
    ``"slugs"`` field, which is ``"slugs": ["slug1", "slug2", "slug3"]``.

    ``slug`` is a string containing the slug of the project to be updated.

    If ``"uri"``, ``"name"``, or ``"owner"`` are set to ``""`` (empty string) or
    ``"slugs"`` is set to ``[]`` (empty array), the value will be set to the
    empty string/array.

    You only need to pass the fields you want to update in ``project``.

    ``project`` accepts the following fields:

    * ``"uri"``
    * ``"name"``
    * ``"slugs"`` - this must be a list of strings
    * ``"owner"``

    Example usage:

    .. code-block:: python

      >>> project = {
      ...    "uri": "https://code.osuosl.org/projects/timesync",
      ...    "name": "pymesync",
      ...}
      >>> ts.update_project(project=project, slug="ps")
      [{'users': {'managers': ['tschuy'], 'spectators': ['tschuy'], 'members': ['patcht', 'tschuy']}, 'uuid': '309eae69-21dc-4538-9fdc-e6892a9c4dd4', 'name': 'pymesync', 'updated_at': '2014-04-18', 'created_at': '2014-04-16', 'deleted_at': None, 'revision': 2, 'uri': 'https://code.osuosl.org/projects/timesync', 'slugs': ['ps']}]
      >>>

------------------------------------------

TimeSync.\ **delete_project(slug)**

    Allows the currently authenticated admin user to delete a project record by
    slug.

    ``slug`` is a string containing the slug of the project to be deleted.

    **delete_project()** returns a ``[{"status": 200}]`` if successful or an
    error message if unsuccessful.

    Example usage:

    .. code-block:: python

      >>> ts.delete_project(slug="some-slug")
      [{"status": 200}]
      >>>

------------------------------------------

TimeSync.\ **create_activity(activity)**

    Create an activity on the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a list with
    a single python dictionary containing the created activity if successful.
    The dictionary will contain error information if ``create_activity()`` was
    unsuccessful.

    ``activity`` is a python dictionary containing the activity information to
    send to TimeSync. The syntax is ``"key": "value"``. ``activity`` requires
    the following fields:

    * ``"name"``
    * ``"slug"``

    Example usage:

    .. code-block:: python

      >>> activity = {
      ...    "name": "Quality Assurance/Testing",
      ...    "slug": "qa"
      ...}
      >>> ts.create_activity(activity=activity)
      [{'uuid': 'cfa07a4f-d446-4078-8d73-2f77560c35c0', 'created_at': '2013-07-27', 'updated_at': None, 'deleted_at': None, 'revision': 1, 'slug': 'qa', 'name': 'Quality Assurance/Testing'}]
      >>>

------------------------------------------

TimeSync.\ **update_activity(activity, slug)**

    Update an existing activity by slug on the TimeSync instance specified by
    the baseurl provided when instantiating the TimeSync object. This method
    will return a list with a single python dictionary containing the updated
    activity if successful. The dictionary will contain error information if
    ``update_activity()`` was unsuccessful.

    ``activity`` is a python dictionary containing the activity information to
    send to TimeSync. The syntax is ``"key": "value"``.

    ``slug`` is a string containing the slug of the activity to be updated.

    If ``"name"`` or ``"slug"`` in ``activity`` are set to ``""`` (empty
    string), the value will be set to the empty string.

    You only need to pass the fields you want to update in ``activity``.

    ``activity`` accepts the following fields to update an activity:

    * ``"name"``
    * ``"slug"``

    Example usage:

    .. code-block:: python

      >>> activity = {"name": "Code in the wild"}
      >>> ts.update_activity(activity=activity, slug="ciw")
      [{'uuid': '3cf78d25-411c-4d1f-80c8-a09e5e12cae3', 'created_at': '2014-04-16', 'updated_at': '2014-04-17', 'deleted_at': None, 'revision': 2, 'slug': 'ciw', 'name': 'Code in the wild'}]
      >>>

------------------------------------------

TimeSync.\ **delete_activity(slug)**

    Allows the currently authenticated admin user to delete an activity record
    by slug.

    ``slug`` is a string containing the slug of the activity to be deleted.

    **delete_activity()** returns a ``[{"status": 200}]`` if successful or an
    error message if unsuccessful.

    Example usage:

    .. code-block:: python

      >>> ts.delete_activity(slug="some-slug")
      [{"status": 200}]
      >>>


------------------------------------------

TimeSync.\ **create_user(user)**

    Create a user on the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a list with
    a single python dictionary containing the created user if successful.
    The dictionary will contain error information if ``create_user()`` was
    unsuccessful.

    ``user`` is a python dictionary containing the user information to send to
    TimeSync. The syntax is ``"key": "value"``. ``user`` requires the following
    fields:

    * ``"username"``
    * ``"password"``

    Additionally, the following parameters may be optionally included:

    * ``"displayname"``
    * ``"email"``

    Example usage:

    .. code-block:: python

      >>> user = {
      ...    "username": "example",
      ...    "password": "password",
      ...    "displayname": "X. Ample User",
      ...    "email": "example@example.com"
      ...}
      >>> ts.create_user(user=user)
      [{'username': 'example', 'deleted_at': None, 'displayname': 'X. Ample User', 'admin': False, 'created_at': '2015-05-23', 'active': True, 'email': 'example@example.com'}]
      >>>

------------------------------------------

TimeSync.\ **update_user(user, username)**

    Update an existing user by ``username`` on the TimeSync instance specified
    by the baseurl provided when instantiating the TimeSync object. This method
    will return a list with a single python dictionary containing the updated
    user if successful. The dictionary will contain error information if
    ``update_user()`` was unsuccessful.

    ``user`` is a python dictionary containing the user information to send to
    TimeSync. The syntax is ``"key": "value"``.

    ``username`` is a string containing the username of the user to be updated.

    You only need to pass the fields you want to update in ``user``.

    ``user`` accepts the following fields to update a user object:

    * ``"username"``
    * ``"password"``
    * ``"displayname"``
    * ``"email"``

    Example usage:

    .. code-block:: python

      >>> user = {
      ...    "username": "red-leader",
      ...    "email": "red-leader@yavin.com"
      ...}
      >>> ts.update_user(user=user, username="example")
      [{'username': 'red-leader', 'displayname': 'Mr. Example', 'admin': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'red-leader@yavin.com'}]
      >>>

------------------------------------------

TimeSync.\ **delete_user(username)**

    Allows the currently authenticated admin user to delete a user record by
    username.

    ``username`` is a string containing the username of the user to be deleted.

    **delete_user()** returns a ``[{"status": 200}]`` if successful or an error
    message if unsuccessful.

    Example usage:

    .. code-block:: python

      >>> ts.delete_user(username="username")
      [{"status": 200}]
      >>>
