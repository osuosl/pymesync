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

All of these methods return a python dictionary (or a list of zero or more
python dictionaries in the case of the ``get_*`` methods).

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

* **get_times(query_parameters)** - Get times from TimeSync
* **get_projects(query_parameters)** - Get project information from TimeSync
* **get_activities(query_parameters)** - Get activity information from TimeSync
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

Pymesync is on PyPi, so you can simply ``pip install pymesync``. We recommend
you use `virtualenv`_, like so:

.. code-block:: none

  virtualenv venv
  source venv/bin/activate
  pip install pymesync

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

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
  pymesync will return this error (get methods will return this error nested in
  a list):

  .. code-block:: python

    {"pymesync error": "Not authenticated with TimeSync, call self.authenticate() first"}

Errors
------

Pymesync returns errors the same way it returns successes for whatever method
is in use. This means that most of the time errors are returned as a Python
dictionary, except in the case of get methods. If the error is a local pymesync
error, the key for the error message will be ``"pymesync error"``. If the error
is from TimeSync, the dictionary will contain the same keys described in the
`TimeSync error documentation`_, but as a python dictionary.

If there is an error connecting with the TimeSync instance specified by the
baseurl passed to the pymesync constructor, the error will also contain the
status code of the response.

An example for a method that returns a dict within a list:

.. code-block:: python

    [{"pymesync error": "connection to TimeSync failed at baseurl http://ts.example.com/v1 - response status was 502"}]

The same error returned from a method that returns a single dict:

.. code-block:: python

    {"pymesync error": "connection to TimeSync failed at baseurl http://ts.example.com/v1 - response status was 502"}

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

    **authenticate()** will return a python dictionary. If authentication was 
    successful, the dictionary will look like this:

    .. code-block:: python

      {"token": "SOMELONGTOKEN"}

    If authentication was unsuccessful, the dict will contain an error message:

    .. code-block:: python

      {"status": 401, "error": "Authentication failure", "text": "Invalid username or password"}

    Example:

    .. code-block:: python

      >>> ts.authenticate(username="example-user", password="example-password", auth_type="password")
      {u'token': u'eyJ0eXAi...XSnv0ghQ=='}
      >>>

TimeSync.\ **token_expiration_time()**

    Returns a python datetime representing the expiration time of the current
    authentication token.

    If an error occurs, the error is returned in a single python dict.

    Example:

    .. code-block:: python

      >>> ts.authenticate(username="username", password="user-pass", auth_type="password")
      {u'token': u'eyJ0eXAiOiJKV1QiLCJhbGciOiJITUFDLVNIQTUxMiJ9.eyJpc3MiOiJvc3Vvc2wtdGltZXN5bmMtc3RhZ2luZyIsInN1YiI6InRlc3QiLCJleHAiOjE0NTI3MTQzMzQwODcsImlhdCI6MTQ1MjcxMjUzNDA4N30=.QP2FbiY3I6e2eN436hpdjoBFbW9NdrRUHbkJ+wr9GK9mMW7/oC/oKnutCwwzMCwjzEx6hlxnGo6/LiGyPBcm3w=='}
      >>> ts.token_expiration_time()
      datetime.datetime(2016, 1, 13, 11, 45, 34)
      >>>

TimeSync.\ **project_users(project)**

    Returns a dictionary containing the user field of the specified project.

    ``project`` is a string containing the desired project slug.

    Example:

    .. code-block:: python

      >> ts.project_users(project="pyme")
      {u'malcolm': [u'member', u'manager'], u'jayne': [u'member'], u'kaylee': [u'member'], u'zoe': [u'member'], u'hoban': [u'member'], u'simon': [u'spectator'], u'river': [u'spectator'], u'derrial': [u'spectator'], u'inara': [u'spectator']}
      >>>

TimeSync.\ **create_time(time)**

    Send a time entry to the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a single python
    dictionary containing the created entry if successful. The dictionary will
    contain error information if ``create_time()`` was unsuccessful.

    ``time`` is a python dictionary containing the time information to send to
    TimeSync. The syntax is ``"string_key": "string_value"`` with the exception
    of the key ``"duration"`` which takes an integer value, and the key
    ``"activities"``, which takes a list of strings containing activity slugs.
    ``create_time()`` accepts the following fields in ``time``:

    Required:

    * ``"duration"`` - duration of time spent working on a project. May be
      entered as a positive integer (which will default to seconds) or a
      string. As a string duration, follow the format ``<val>h<val>m``. An
      internal method will convert the duration to seconds.
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
      {u'activities': [u'docs'], u'deleted_at': None, u'date_worked': u'2014-04-17', u'uuid': u'838853e3-3635-4076-a26f-7efr4e60981f', u'notes': u'Worked on documentation toward settings configuration.', u'updated_at': None, u'project': u'ganeti_web_manager', u'user': u'example-2', u'duration': 1200, u'issue_uri': u'https://github.com/osuosl/ganeti_webmgr/issues', u'created_at': u'2015-05-23', u'revision': 1}
      >>>

    .. code-block:: python

      >>> time = {
      ...    "duration": "3h30m",
      ...    "user": "example-2",
      ...    "project": "ganeti_web_manager",
      ...    "activities": ["docs"],
      ...    "notes": "Worked on documentation toward settings configuration.",
      ...    "issue_uri": "https://github.com/osuosl/ganeti_webmgr/issues",
      ...    "date_worked": "2014-04-17"
      ...}
      >>> ts.create_time(time=time)
      {u'activities': [u'docs'], u'deleted_at': None, u'date_worked': u'2014-04-17', u'uuid': u'838853e3-3635-4076-a26f-7efr4e60981f', u'notes': u'Worked on documentation toward settings configuration.', u'updated_at': None, u'project': u'ganeti_web_manager', u'user': u'example-2', u'duration': 12600, u'issue_uri': u'https://github.com/osuosl/ganeti_webmgr/issues', u'created_at': u'2015-05-23', u'revision': 1}
      >>>

------------------------------------------

TimeSync.\ **update_time(time, uuid)**

    Update a time entry by uuid on the TimeSync instance specified by the
    baseurl provided when instantiating the TimeSync object. This method will
    return a python dictionary containing the updated entry if successful. The
    dictionary will contain error information if ``update_time()`` was
    unsuccessful.

    ``time`` is a python dictionary containing the time information to send to
    TimeSync. The syntax is ``"string_key": "string_value"`` with the exception
    of the key ``"duration"`` which takes an integer value, and the key
    ``"activities"``, which takes a list of strings containing activity slugs.
    You only need to send the fields that you want to update.

    ``uuid`` is a string containing the uuid of the time to be updated.

    ``update_time()`` accepts the following fields in ``time``:

    * ``"duration"`` - duration of time spent working on a project. May be
      entered as a positive integer (which will default to seconds) or a
      string. As a string duration, follow the format ``<val>h<val>m``. An
      internal method will convert the duration to seconds.
    * ``"project"`` - slug of project worked on
    * ``"user"`` - username of user that did the work, must match ``user``
      specified in ``authenticate()``
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
      {u'activities': [u'hello', u'world'], u'date_worked': u'2015-08-07', u'updated_at': u'2015-10-18', u'user': u'red-leader', u'duration': 1900, u'deleted_at': None, u'uuid': u'some-uuid', u'notes': None, u'project': [u'ganeti'], u'issue_uri': u'https://github.com/osuosl/ganeti_webmgr/issues/56', u'created_at': u'2014-06-12', u'revision': 2}

      >>> time = {
      ...    "duration": "3h35m",
      ...    "user": "red-leader",
      ...    "activities": ["hello", "world"],
      ...}
      >>> ts.update_time(time=time, uuid="some-uuid")
      {u'activities': [u'hello', u'world'], u'date_worked': u'2015-08-07', u'updated_at': u'2015-10-18', u'user': u'red-leader', u'duration': 12900, u'deleted_at': None, u'uuid': u'some-uuid', u'notes': None, u'project': [u'ganeti'], u'issue_uri': u'https://github.com/osuosl/ganeti_webmgr/issues/56', u'created_at': u'2014-06-12', u'revision': 3}

------------------------------------------

TimeSync.\ **get_times(query_parameters=None)**

    Request time entries from the TimeSync instance specified by the baseurl
    provided when instantiating the TimeSync object. The time entries are
    filtered by parameters passed in ``query_parameters``. Returns a list of
    python dictionaries containing the time information returned by TimeSync or
    an error message if unsuccessful.

    ``query_parameters`` is a python dictionary containing the optional query
    parameters described in the `TimeSync documentation`_. If
    ``query_parameters`` is missing, it defaults to ``None``, in which case
    ``get_times()`` will return all times the current user is authorized to see.
    The syntax for each argument is ``{"query": ["parameter1", "parameter2"]}``
    except for the ``uuid`` parameter which is ``{"uuid": "uuid-as-string"}``
    and the ``include_deleted`` and ``include_revisions`` parameters which
    should be set to booleans.

    Currently the valid queries allowed by pymesync are:

    * ``user`` - filter time request by username

      - example: ``{"user": ["username"]}``

    * ``project`` - filter time request by project slug

      - example: ``{"project": ["slug"]}``

    * ``activity`` - filter time request by activity slug

      - example: ``{"activity": ["slug"]}``

    * ``start`` - filter time request by start date

      - example: ``{"start": ["2014-07-23"]}``

    * ``end`` - filter time request by end date

      - example: ``{"end": ["2015-07-23"]}``

    * ``include_revisions`` - either ``True`` or ``False`` to include
      revisions of times. Defaults to ``False``

      - example: ``{"include_revisions": True}``

    * ``include_deleted`` - either ``True`` or ``False`` to include
      deleted times. Defaults to ``False``

      - example: ``{"include_deleted": True}``

    * ``uuid`` - get specific time entry by time uuid

      - example: ``{"uuid": "someuuid"}``

      To get a deleted time by ``uuid``, also add the ``include_deleted``
      parameter.

    Example usage:

    .. code-block:: python

      >>> ts.get_times()
      [{u'activities': [u'docs', u'planning'], u'date_worked': u'2014-04-17', u'updated_at': None, u'user': u'userone', u'duration': 1200, u'deleted_at': None, u'uuid': u'c3706e79-1c9a-4765-8d7f-89b4544cad56', u'notes': u'Worked on documentation.', u'project': [u'ganeti-webmgr', u'gwm'], u'issue_uri': u'https://github.com/osuosl/ganeti_webmgr', u'created_at': u'2014-04-17', u'revision': 1}, {u'activities': [u'code', u'planning'], u'date_worked': u'2014-04-17', u'updated_at': None, u'user': u'usertwo', u'duration': 1300, u'deleted_at': None, u'uuid': u'12345676-1c9a-rrrr-bbbb-89b4544cad56', u'notes': u'Worked on coding', u'project': [u'ganeti-webmgr', u'gwm'], u'issue_uri': u'https://github.com/osuosl/ganeti_webmgr', u'created_at': u'2014-04-17', u'revision': 1}, {u'activities': [u'code'], u'date_worked': u'2014-04-17', u'updated_at': None, u'user': u'userthree', u'duration': 1400, u'deleted_at': None, u'uuid': u'12345676-1c9a-ssss-cccc-89b4544cad56', u'notes': u'Worked on coding', u'project': [u'timesync', u'ts'], u'issue_uri': u'https://github.com/osuosl/timesync', u'created_at': u'2014-04-17', u'revision': 1}]
      >>>

    .. warning::

      If the ``uuid`` parameter is passed all other parameters will be ignored
      except for ``include_deleted`` and ``include_revisions``. For example,
      ``ts.get_times({"uuid": "time-entry-uuid", "user": ["bob", "rob"]})`` is
      equivalent to ``ts.get_times({"uuid": "time-entry-uuid"})``.

------------------------------------------

TimeSync.\ **delete_time(uuid)**

    Allows the currently authenticated user to delete their own time entry by
    uuid.

    ``uuid`` is a string containing the uuid of the time entry to be deleted.

    **delete_time()** returns a ``{"status": 200}`` if successful or an error
    message if unsuccessful.

    Example usage:

    .. code-block:: python

      >>> ts.delete_time(uuid="some-uuid")
      {"status": 200}
      >>>

------------------------------------------

TimeSync.\ **get_projects(query_parameters=None)**

    Request project entries from the TimeSync instance specified by the baseurl
    provided when instantiating the TimeSync object. The project entries are
    filtered by parameters passed in ``query_parameters``. Returns a list of
    python dictionaries containing the project information returned by TimeSync
    or an error message if unsuccessful.

    ``query_parameters`` is a dict containing the optional query parameters
    described in the `TimeSync documentation`_. If ``query_parameters`` is
    empty, ``get_projects()`` will return all projects in the database. The
    syntax for each argument is ``{"query": "parameter"}`` or
    ``{"bool_query": <boolean>}``.

    The optional parameters currently supported by the TimeSync API are:

    * ``slug`` - filter project request by project slug

      - example: ``{"slug": "gwm"}``

    * ``include_deleted`` - tell TimeSync whether to include deleted projects in
      request. Default is ``False`` and cannot be combined with a ``slug``.

      - example: ``{"include_deleted": True}``

    * ``include_revisions`` - tell TimeSync whether to include past revisions of
      projects in request. Default is ``False``

      - example: ``{"include_revisions": True}``

    Example usage:

    .. code-block:: python

      >>> ts.get_projects()
      [{u'users': {u'tschuy': {u'member': true, u'spectator': false, u'manager': false}, u'mrsj': {u'member': true, u'spectator': false, u'manager': true}, u'oz': {u'member': false, u'spectator': true, u'manager': false}}, u'uuid': u'a034806c-00db-4fe1-8de8-514575f31bfb', u'deleted_at': None, u'name': u'Ganeti Web Manager', u'updated_at': u'2014-07-20', u'created_at': u'2014-07-17', u'revision': 4, u'uri': u'https://code.osuosl.org/projects/ganeti-webmgr', u'slugs': [u'gwm']}, {u'users': {u'managers': [u'tschuy'], u'spectators': [u'tschuy', u'mrsj'], u'members': [u'patcht', u'tschuy', u'mrsj']}, u'uuid': u'a034806c-rrrr-bbbb-8de8-514575f31bfb', u'deleted_at': None, u'name': u'TimeSync', u'updated_at': u'2014-07-20', u'created_at': u'2014-07-17', u'revision': 2, u'uri': u'https://code.osuosl.org/projects/timesync', u'slugs': [u'timesync', u'ts']}, {u'users': {u'managers': [u'mrsj'], u'spectators': [u'tschuy', u'mrsj'], u'members': [u'patcht', u'tschuy', u'mrsj', u'MaraJade', u'thai']}, u'uuid': u'a034806c-ssss-cccc-8de8-514575f31bfb', u'deleted_at': None, u'name': u'pymesync', u'updated_at': u'2014-07-20', u'created_at': u'2014-07-17', u'revision': 1, u'uri': u'https://code.osuosl.org/projects/pymesync', u'slugs': [u'pymesync', u'ps']}]
      >>>

    .. warning::

      Does not accept a ``slug`` combined with ``include_deleted``, but does
      accept any other combination.

------------------------------------------

TimeSync.\ **get_activities(query_parameters=None)**

    Request activity entries from the TimeSync instance specified by the baseurl
    provided when instantiating the TimeSync object. The activity entries are
    filtered by parameters passed in ``query_parameters``. Returns a list of
    python dictionaries containing the activity information returned by TimeSync
    or an error message if unsuccessful.

    ``query_parameters`` contains the optional query parameters described in the
    `TimeSync documentation`_. If ``query_parameters`` is empty,
    ``get_activities()`` will return all activities in the database. The syntax
    for each argument is ``{"query": "parameter"}`` or
    ``{"bool_query": <boolean>}``.

    The optional parameters currently supported by the TimeSync API are:

    * ``slug`` - filter activity request by activity slug

      - example: ``{"slug": "code"}``

    * ``include_deleted`` - tell TimeSync whether to include deleted activities
      in request. Default is ``False`` and cannot be combined with a ``slug``.

      - example: ``{"include_deleted": True}``

    * ``include_revisions`` - tell TimeSync whether to include past revisions of
      activities in request. Default is ``False``

      - example: ``{"include_revisions": True}``

    Example usage:

    .. code-block:: python

      >>> ts.get_activities()
      [{u'uuid': u'adf036f5-3d49-4a84-bef9-062b46380bbf', u'created_at': u'2014-04-17', u'updated_at': None, u'name': u'Documentation', u'deleted_at': None, u'slugs': [u'docs'], u'revision': 5}, {u'uuid': u'adf036f5-3d49-bbbb-rrrr-062b46380bbf', u'created_at': u'2014-04-17', u'updated_at': None, u'name': u'Coding', u'deleted_at': None, u'slugs': [u'code', u'dev'], u'revision': 1}, {u'uuid': u'adf036f5-3d49-cccc-ssss-062b46380bbf', u'created_at': u'2014-04-17', u'updated_at': None, u'name': u'Planning', u'deleted_at': None, u'slugs': [u'plan', u'prep'], u'revision': 1}]
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
      [{u'username': u'userone', u'displayname': u'One Is The Loneliest Number', u'admin': False, u'created_at': u'2015-02-29', u'active': True, u'deleted_at': None, u'email': u'exampleone@example.com'}, {u'username': u'usertwo', u'displayname': u'Two Can Be As Bad As One', u'admin': False, u'created_at': u'2015-02-29', u'active': True, u'deleted_at': None, u'email': u'exampletwo@example.com'}, {u'username': u'userthree', u'displayname': u'Yes Its The Saddest Experience', u'admin': False, u'created_at': u'2015-02-29', u'active': True, u'deleted_at': None, u'email': u'examplethree@example.com'}, {u'username': u'userfour', u'displayname': u'Youll Ever Do', u'admin': False, u'created_at': u'2015-02-29', u'active': True, u'deleted_at': None, u'email': u'examplefour@example.com'}]
      >>>

------------------------------------------

.. _TimeSync documentation: http://timesync.readthedocs.org/en/latest/draft_api.html#get-endpoints

Administrative methods
----------------------

These methods are available to TimeSync users with administrative permissions.

TimeSync.\ **create_project(project)**

    Create a project on the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a single python
    dictionary containing the created project if successful. The dictionary
    will contain error information if ``create_project()`` was unsuccessful.

    ``project`` is a python dictionary containing the project information to
    send to TimeSync. The syntax is ``"key": "value"`` except for the
    ``"slugs"`` field, which is ``"slugs": ["slug1", "slug2", "slug3"]``.
    ``project`` requires the following fields:

    * ``"uri"``
    * ``"name"``
    * ``"slugs"`` - this must be a list of strings

    Optionally include a users field to add users to the project:

    * ``"users"`` - this must be a python dictionary containing individual user
                    permissions. See example below.

    Example usage:

    .. code-block:: python

      >>> project = {
      ...    "uri": "https://code.osuosl.org/projects/timesync",
      ...    "name": "TimeSync API",
      ...    "slugs": ["timesync", "time"],
      ...    "users": {"tschuy": {"member": True, "spectator": False, "manager": True},
      ...              "mrsj": {"member": True, "spectator": False, "manager": False},
      ...              "patcht": {"member": True, "spectator": False, "manager": True},
      ...              "oz": {"member": False, "spectator": True, "manager": False}
      ...             }
      ...}
      >>>
      >>> ts.create_project(project=project)
      {u'users': {u'tschuy': {u'member': true, u'spectator': false, u'manager': true}, u'mrsj': {u'member': true, u'spectator': false, u'manager': false}, u'patcht': {u'member': true, u'spectator': false, u'manager': true}, u'oz': {u'member': false, u'spectator': true, u'manager': false}}, u'deleted_at': None, u'uuid': u'309eae69-21dc-4538-9fdc-e6892a9c4dd4', u'updated_at': None, u'created_at': u'2015-05-23', u'uri': u'https://code.osuosl.org/projects/timesync', u'name': u'TimeSync API', u'revision': 1, u'slugs': [u'timesync', u'time']}
      >>>

------------------------------------------

TimeSync.\ **update_project(project, slug)**

    Update an existing project by slug on the TimeSync instance specified by the
    baseurl provided when instantiating the TimeSync object. This method will
    return a python dictionary containing the updated project if successful.
    The dictionary will contain error information if ``update_project()`` was
    unsuccessful.

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
    * ``"user"``

    Example usage:

    .. code-block:: python

      >>> project = {
      ...    "uri": "https://code.osuosl.org/projects/timesync",
      ...    "name": "pymesync",
      ...}
      >>> ts.update_project(project=project, slug="ps")
      {u'users': {u'tschuy': {u'member': True, u'spectator': True, u'manager': True}, u'patcht': {u'member': True, u'spectator': False, u'manager': False}}, u'uuid': u'309eae69-21dc-4538-9fdc-e6892a9c4dd4', u'name': u'pymesync', u'updated_at': u'2014-04-18', u'created_at': u'2014-04-16', u'deleted_at': None, u'revision': 2, u'uri': u'https://code.osuosl.org/projects/timesync', u'slugs': [u'ps']}
      >>>

------------------------------------------

TimeSync.\ **delete_project(slug)**

    Allows the currently authenticated admin user to delete a project record by
    slug.

    ``slug`` is a string containing the slug of the project to be deleted.

    **delete_project()** returns a ``{"status": 200}`` if successful or an
    error message if unsuccessful.

    Example usage:

    .. code-block:: python

      >>> ts.delete_project(slug="some-slug")
      {u'status': 200}
      >>>

------------------------------------------

TimeSync.\ **create_activity(activity)**

    Create an activity on the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a python
    dictionary containing the created activity if successful. The dictionary
    will contain error information if ``create_activity()`` was unsuccessful.

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
      {u'uuid': u'cfa07a4f-d446-4078-8d73-2f77560c35c0', u'created_at': u'2013-07-27', u'updated_at': None, u'deleted_at': None, u'revision': 1, u'slug': u'qa', u'name': u'Quality Assurance/Testing'}
      >>>

------------------------------------------

TimeSync.\ **update_activity(activity, slug)**

    Update an existing activity by slug on the TimeSync instance specified by
    the baseurl provided when instantiating the TimeSync object. This method
    will return a python dictionary containing the updated activity if
    successful. The dictionary will contain error information if
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
      {u'uuid': u'3cf78d25-411c-4d1f-80c8-a09e5e12cae3', u'created_at': u'2014-04-16', u'updated_at': u'2014-04-17', u'deleted_at': None, u'revision': 2, u'slug': u'ciw', u'name': u'Code in the wild'}
      >>>

------------------------------------------

TimeSync.\ **delete_activity(slug)**

    Allows the currently authenticated admin user to delete an activity record
    by slug.

    ``slug`` is a string containing the slug of the activity to be deleted.

    **delete_activity()** returns a ``{"status": 200}`` if successful or an
    error message if unsuccessful.

    Example usage:

    .. code-block:: python

      >>> ts.delete_activity(slug="some-slug")
      {u'status': 200}
      >>>


------------------------------------------

TimeSync.\ **create_user(user)**

    Create a user on the TimeSync instance at the baseurl provided when
    instantiating the TimeSync object. This method will return a python
    dictionary containing the created user if successful. The dictionary will
    contain error information if ``create_user()`` was unsuccessful.

    ``user`` is a python dictionary containing the user information to send to
    TimeSync. The syntax is ``"key": "value"``. ``user`` requires the following
    fields:

    * ``"username"``
    * ``"password"``

    Additionally, the following parameters may be optionally included:

    * ``"displayname"``
    * ``"email"``
    * ``"admin"`` - sitewide permission, must be a boolean
    * ``"spectator"`` - sitewide permission , must be a boolean
    * ``"manager"`` - sitewide permission, must be a boolean
    * ``"active"`` - user status, usually set internally, must be a boolean

    Example usage:

    .. code-block:: python

      >>> user = {
      ...    "username": "example",
      ...    "password": "password",
      ...    "displayname": "X. Ample User",
      ...    "email": "example@example.com"
      ...}
      >>> ts.create_user(user=user)
      {u'username': u'example', u'deleted_at': None, u'displayname': u'X. Ample User', u'admin': False, u'created_at': u'2015-05-23', u'active': True, u'email': u'example@example.com'}
      >>>

------------------------------------------

TimeSync.\ **update_user(user, username)**

    Update an existing user by ``username`` on the TimeSync instance specified
    by the baseurl provided when instantiating the TimeSync object. This method
    will return a python dictionary containing the updated user if successful.
    The dictionary will contain error information if ``update_user()`` was
    unsuccessful.

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
      {u'username': u'red-leader', u'displayname': u'Mr. Example', u'admin': False, u'created_at': u'2015-02-29', u'active': True, u'deleted_at': None, u'email': u'red-leader@yavin.com'}
      >>>

------------------------------------------

TimeSync.\ **delete_user(username)**

    Allows the currently authenticated admin user to delete a user record by
    username.

    ``username`` is a string containing the username of the user to be deleted.

    **delete_user()** returns a ``{"status": 200}`` if successful or an error
    message if unsuccessful.

    Example usage:

    .. code-block:: python

      >>> ts.delete_user(username="username")
      {u'status": 200}
      >>>
