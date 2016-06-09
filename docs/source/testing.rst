.. _testing:

Testing Code That Uses Pymesync
===============================

.. contents::

Testing code that calls external modules can be difficult if those modules make
expensive API calls, like pymesync. Often, the code that uses pymesync relies
on the data that pymesync/TimeSync returns, so mocking pymesync is unrealistic.

Because of this, pymesync has a built-in test mode that allows users of the
module to test their code. When in test mode, pymesync returns *representations*
of what would be returned upon a successful TimeSync API call. Pymesync still
runs all internal error checking while in test mode.

To start test mode, it must be set in the constructor with ``test=True``:

.. code-block:: python

  >>> import pymesync
  >>>
  >>> ts = pymesync.TimeSync(baseurl="http://timesync.example.com/v1", test=True)
  >>> ts.authenticate(username="test-user", password="test-password", auth_type="password")
  [{'token': 'TESTTOKEN'}]
  >>>

Individual methods, like ``create_time()``, take all the parameters specified in
:ref:`usage`. In test mode, those methods return valid representations of
TimeSync objects (according to the `TimeSync API`_) using the data that was
passed to pymesync.

An (almost) exhaustive example of test mode:

.. code-block:: python

  >>> import pymesync
  >>>
  >>> ts = pymesync.TimeSync(baseurl="http://timesync.example.com/v1", test=True)
  >>>
  >>> time = {
  ...    "duration": 12,
  ...    "user": "example-2",
  ...    "project": "ganeti_web_manager",
  ...    "activities": ["docs"],
  ...    "notes": "Worked on documentation toward settings configuration.",
  ...    "issue_uri": "https://github.com/osuosl/ganeti_webmgr/issues",
  ...    "date_worked": "2014-04-17"
  ...}
  >>> ts.create_time(time=time)
  [{'pymesync error': 'Not authenticated with TimeSync, call self.authenticate() first'}]
  >>>
  >>> ts.authenticate(username="test-user", password="test-pass", auth_type="password")
  [{'token': 'TESTTOKEN'}]
  >>>
  >>> ts.token_expiration_time()
  datetime.datetime(2016, 1, 13, 11, 45, 34)
  >>>
  >>> ts.create_time(time=time)
  [{'activities': ['docs'], 'deleted_at': None, 'date_worked': '2014-04-17', 'uuid': '838853e3-3635-4076-a26f-7efr4e60981f', 'notes': 'Worked on documentation toward settings configuration.', 'updated_at': None, 'project': 'ganeti_web_manager', 'user': 'example-2', 'duration': 12, 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr/issues', 'created_at': '2014-04-17', 'revision': 1}]
  >>>
  >>> time = {
  ...    "duration": 19,
  ...    "user": "red-leader",
  ...    "activities": ["hello", "world"],
  ...}
  >>> ts.update_time(time=time, uuid="some-uuid")
  [{'activities': ['hello', 'world'], 'date_worked': '2015-08-07', 'updated_at': '2015-10-18', 'user': 'red-leader', 'duration': 19, 'deleted_at': None, 'uuid': 'some-uuid', 'notes': None, 'project': ['ganeti'], 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr/issues/56', 'created_at': '2014-06-12', 'revision': 2}]
  >>>
  >>> time = {
  ...    "duration": "0h30m",
  ...    "user": "red-leader",
  ...    "project": "ganeti_web_manager",
  ...    "activities": ["docs"],
  ...    "notes": "Worked on documentation toward settings configuration.",
  ...    "issue_uri": "https://github.com/osuosl/ganeti_webmgr/issues",
  ...    "date_worked": "2014-04-17"
  ...}

  >>> ts.create_time(time=time)
  [{'activities': ['docs'], 'deleted_at': None, 'date_worked': '2014-04-17', 'uuid': '838853e3-3635-4076-a26f-7efr4e60981f', 'notes': 'Worked on documentation toward settings configuration.', 'updated_at': None, 'project': 'ganeti_web_manager', 'user': 'red-leader', 'duration': '1800', 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr/issues', 'created_at': '2014-04-17', 'revision': 1}]
  >>>
  >>> time = {
  ...    "duration": "1h50m",
  ...    "user": "red-leader",
  ...    "activities": ["hello", "world"],
  ...}
  >>> ts.update_time(time=time, uuid="some-uuid")
  [{'activities': ['hello', 'world'], 'date_worked': '2015-08-07', 'updated_at': '2015-10-18', 'user': 'red-leader', 'duration': '6600', 'deleted_at': None, 'uuid': 'some-uuid', 'notes': None, 'project': ['ganeti'], 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr/issues/56', 'created_at': '2014-06-12', 'revision': 2}]
  >>>
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
  [{'users': {'tschuy': {'member': true, 'spectator': false, 'manager': true}, 'mrsj': {'member': true, 'spectator': false, 'manager': false}, 'patcht': {'member': true, 'spectator': false, 'manager': true}, 'oz': {'member': false, 'spectator': true, 'manager': false}}, 'deleted_at': None, 'uuid': '309eae69-21dc-4538-9fdc-e6892a9c4dd4', 'updated_at': None, 'created_at': '2015-05-23', 'uri': 'https://code.osuosl.org/projects/timesync', 'name': 'TimeSync API', 'revision': 1, 'slugs': ['timesync', 'time'], 'users': {'managers': ['tschuy'], 'spectators': ['tschuy'], 'members': ['patcht', 'tschuy']}}]
  >>>
  >>> project = {
  ...    "uri": "https://code.osuosl.org/projects/timesync",
  ...    "name": "pymesync",
  ...}
  >>> ts.update_project(project=project, slug="ps")
  [{'users': {'tschuy': {'member': true, 'spectator': true, 'manager': false}, 'mrsj': {'member': true, 'spectator': false, 'manager': true}}, 'uuid': '309eae69-21dc-4538-9fdc-e6892a9c4dd4', 'name': 'pymesync', 'updated_at': '2014-04-18', 'created_at': '2014-04-16', 'deleted_at': None, 'revision': 2, 'uri': 'https://code.osuosl.org/projects/timesync', 'slugs': ['ps']}]
  >>>
  >>> activity = {
  ...    "name": "Quality Assurance/Testing",
  ...    "slug": "qa"
  ...}
  >>> ts.create_activity(activity=activity)
  [{'uuid': 'cfa07a4f-d446-4078-8d73-2f77560c35c0', 'created_at': '2013-07-27', 'updated_at': None, 'deleted_at': None, 'revision': 1, 'slug': 'qa', 'name': 'Quality Assurance/Testing'}]
  >>>
  >>> activity = {"name": "Code in the wild"}
  >>> ts.update_activity(activity=activity, slug="ciw")
  [{'uuid': '3cf78d25-411c-4d1f-80c8-a09e5e12cae3', 'created_at': '2014-04-16', 'updated_at': '2014-04-17', 'deleted_at': None, 'revision': 2, 'slug': 'ciw', 'name': 'Code in the wild'}]
  >>>
  >>> user = {
  ...    "username": "example",
  ...    "password": "password",
  ...    "display_name": "X. Ample User",
  ...    "email": "example@example.com"
  ...}
  >>> ts.create_user(user=user)
  [{'username': 'example', 'deleted_at': None, 'display_name': 'X. Ample User', 'site_manager': False, 'site_spectator': False, 'site_admin': False, 'created_at': '2015-05-23', 'active': True, 'email': 'example@example.com'}]
  >>>
  >>> user = {
  ...    "username": "red-leader",
  ...    "email": "red-leader@yavin.com"
  ...}
  >>> ts.update_user(user=user, username="example")
  [{'username': 'red-leader', 'display_name': 'Mr. Example', 'site_manager': False, 'site_spectator': False, 'site_admin': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'red-leader@yavin.com'}]
  >>>
  >>> ts.get_times()
  [{'activities': ['docs', 'planning'], 'date_worked': '2014-04-17', 'updated_at': None, 'user': 'userone', 'duration': 12, 'deleted_at': None, 'uuid': 'c3706e79-1c9a-4765-8d7f-89b4544cad56', 'notes': 'Worked on documentation.', 'project': ['ganeti-webmgr', 'gwm'], 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr', 'created_at': '2014-04-17', 'revision': 1}, {'activities': ['code', 'planning'], 'date_worked': '2014-04-17', 'updated_at': None, 'user': 'usertwo', 'duration': 13, 'deleted_at': None, 'uuid': '12345676-1c9a-rrrr-bbbb-89b4544cad56', 'notes': 'Worked on coding', 'project': ['ganeti-webmgr', 'gwm'], 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr', 'created_at': '2014-04-17', 'revision': 1}, {'activities': ['code'], 'date_worked': '2014-04-17', 'updated_at': None, 'user': 'userthree', 'duration': 14, 'deleted_at': None, 'uuid': '12345676-1c9a-ssss-cccc-89b4544cad56', 'notes': 'Worked on coding', 'project': ['timesync', 'ts'], 'issue_uri': 'https://github.com/osuosl/timesync', 'created_at': '2014-04-17', 'revision': 1}]
  >>>
  >>> ts.get_projects()
  [{'users': {'managers': ['tschuy'], 'spectators': ['tschuy'], 'members': ['patcht', 'tschuy']}, 'uuid': 'a034806c-00db-4fe1-8de8-514575f31bfb', 'deleted_at': None, 'name': 'Ganeti Web Manager', 'updated_at': '2014-07-20', 'created_at': '2014-07-17', 'revision': 4, 'uri': 'https://code.osuosl.org/projects/ganeti-webmgr', 'slugs': ['gwm']}, {'users': {'managers': ['tschuy'], 'spectators': ['tschuy', 'mrsj'], 'members': ['patcht', 'tschuy', 'mrsj']}, 'uuid': 'a034806c-rrrr-bbbb-8de8-514575f31bfb', 'deleted_at': None, 'name': 'TimeSync', 'updated_at': '2014-07-20', 'created_at': '2014-07-17', 'revision': 2, 'uri': 'https://code.osuosl.org/projects/timesync', 'slugs': ['timesync', 'ts']}, {'users': {'managers': ['mrsj'], 'spectators': ['tschuy', 'mrsj'], 'members': ['patcht', 'tschuy', 'mrsj', 'MaraJade', 'thai']}, 'uuid': 'a034806c-ssss-cccc-8de8-514575f31bfb', 'deleted_at': None, 'name': 'pymesync', 'updated_at': '2014-07-20', 'created_at': '2014-07-17', 'revision': 1, 'uri': 'https://code.osuosl.org/projects/pymesync', 'slugs': ['pymesync', 'ps']}]
  >>>
  >>> ts.get_activities()
  [{'uuid': 'adf036f5-3d49-4a84-bef9-062b46380bbf', 'created_at': '2014-04-17', 'updated_at': None, 'name': 'Documentation', 'deleted_at': None, 'slugs': ['docs'], 'revision': 5}, {'uuid': 'adf036f5-3d49-bbbb-rrrr-062b46380bbf', 'created_at': '2014-04-17', 'updated_at': None, 'name': 'Coding', 'deleted_at': None, 'slugs': ['code', 'dev'], 'revision': 1}, {'uuid': 'adf036f5-3d49-cccc-ssss-062b46380bbf', 'created_at': '2014-04-17', 'updated_at': None, 'name': 'Planning', 'deleted_at': None, 'slugs': ['plan', 'prep'], 'revision': 1}]
  >>>
  >>> ts.get_users()
  [{'username': 'userone', 'display_name': 'One Is The Loneliest Number', 'site_manager': False, 'site_admin': False, 'site_spectator': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'exampleone@example.com'}, {'username': 'usertwo', 'display_name': 'Two Can Be As Bad As One', 'site_admin': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'exampletwo@example.com'}, {'username': 'userthree', 'display_name': "Yes It's The Saddest Experience", 'site_admin': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'examplethree@example.com'}, {'username': 'userfour', 'display_name': "You'll Ever Do", 'site_admin': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'examplefour@example.com'}]
  >>>
  >>> ts.get_users("admin")
  [{'username': 'admin', 'display_name': 'X. Ample User', 'site_manager': False, 'site_admin': True, 'site_spectator': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'example@example.com'}]
  >>>
  >>> ts.get_users("manager")
  [{'username': 'manager', 'display_name': 'X. Ample User', 'site_manager': True, 'site_admin': False, 'site_spectator': False, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'example@example.com'}]
  >>>
  >>> ts.get_users("spectator")
  [{'username': 'spectator', 'display_name': 'X. Ample User', 'site_manager': False, 'site_admin': False, 'site_spectator': True, 'created_at': '2015-02-29', 'active': True, 'deleted_at': None, 'email': 'example@example.com'}]
  >>>
  >>> ts.get_times({"uuid": "some-uuid"})
  [{'activities': ['docs', 'planning'], 'date_worked': '2014-04-17', 'updated_at': None, 'user': 'userone', 'duration': 12, 'deleted_at': None, 'uuid': 'some-uuid', 'notes': 'Worked on documentation.', 'project': ['ganeti-webmgr', 'gwm'], 'issue_uri': 'https://github.com/osuosl/ganeti_webmgr', 'created_at': '2014-04-17', 'revision': 1}]
  >>>
  >>> ts.delete_time(uuid="some-uuid")
  [{"status": 200}]
  >>>
  >>> ts.delete_user(username="username")
  [{"status": 200}]
  >>>
  >>> ts.project_users(project="ff")
  {'malcolm': ['member', 'manager'], 'jayne': ['member'], 'kaylee': ['member'], 'zoe': ['member'], 'hoban': ['member'], 'simon': ['spectator'], 'river': ['spectator'], 'derrial': ['spectator'], 'inara': ['spectator']}
  >>>


.. _TimeSync API: http://timesync.readthedocs.org/en/latest/
