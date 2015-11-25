import unittest
import pymesync
import mock
import requests


class TestPymesync(unittest.TestCase):

    def test_send_time_valid(self):
        """Tests TimeSync.send_time with valid data"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        # Test baseurl
        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Format content for assert_called_with test
        content = {
            'auth': ts._auth(),
            'object': params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        ts.send_time(params)

        patched_json_loader.stop()

        # Test it
        requests.post.assert_called_with('http://ts.example.com/v1/times',
                                         json=content)

    def test_send_time_catch_request_error(self):
        """Tests TimeSync.send_time with request error"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
            "project": "ganet_web_manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        # Test baseurl
        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        self.assertRaises(Exception, ts.send_time(params))

    def test_auth(self):
        """Tests TimeSync._auth function"""
        # Test baseurl
        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Create auth block to test _auth
        auth = {'type': "password",
                'username': "example-user",
                'password': "password", }

        self.assertEquals(ts._auth(), auth)

    def test_get_time_for_user(self):
        """Tests TimeSync.get_times with username query parameter"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(user=[ts.user])

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?user=example-user')

    def test_get_time_for_proj(self):
        """Tests TimeSync.get_times with project query parameter"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(project=["gwm"])

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?project=gwm')

    def test_get_time_for_activity(self):
        """Tests TimeSync.get_times with activity query parameter"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(activity=["dev"])

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?activity=dev')

    def test_get_time_for_start_date(self):
        """Tests TimeSync.get_times with start date query parameter"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(start=["2015-07-23"])

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?start=2015-07-23')

    def test_get_time_for_end_date(self):
        """Tests TimeSync.get_times with end date query parameter"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(end=["2015-07-23"])

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?end=2015-07-23')

    def test_get_time_for_revisions(self):
        """Tests TimeSync.get_times with revisions query parameter"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(revisions=["true"])

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?revisions=true')

    def test_get_time_for_proj_and_activity(self):
        """Tests TimeSync.get_times with project and activity query
        parameters"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(project=["gwm"], activity=["dev"])

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameters
        # Multiple paramaters are sorted alphabetically
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?activity=dev&project=gwm')

    def test_get_time_for_activity_x3(self):
        """Tests TimeSync.get_times with project and activity query
        parameters"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(activity=["dev", "rev", "hd"])

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameters
        # Multiple paramaters are sorted alphabetically
        requests.get.assert_called_with("http://ts.example.com/v1/times"
                                        + "?activity=dev"
                                        + "&activity=rev"
                                        + "&activity=hd")

    def test_get_time_with_id(self):
        """Tests TimeSync.get_times with revisions query parameter"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(id=2)

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times/2')

    def test_get_time_with_id_and_activity(self):
        """Tests TimeSync.get_times with revisions query parameter"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(id=3, activity=["dev"])

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times/3')

    def test_get_all_times(self):
        """Tests TimeSync.get_times with no paramaters"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times()

        patched_json_loader.stop()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with('http://ts.example.com/v1/times')

    def test_get_times_bad_param(self):
        """Tests TimeSync.get_times with an invalid query parameter"""
        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Should return the error
        self.assertEquals({'pymesync error': 'invalid query: bad'},
                          ts.get_times(bad=["query"]))

    def test_get_projects(self):
        """Tests TimeSync.get_projects"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_projects()

        patched_json_loader.stop()

        # Test that requests.get was called correctly
        requests.get.assert_called_with('http://ts.example.com/v1/projects')

    def test_get_projects_slug(self):
        """Tests TimeSync.get_projects with slug"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_projects(slug='gwm')

        patched_json_loader.stop()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(
            'http://ts.example.com/v1/projects/gwm')

    def test_get_projects_revisions(self):
        """Tests TimeSync.get_projects with revisions query"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_projects(revisions=True)

        patched_json_loader.stop()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(
            'http://ts.example.com/v1/projects?revisions=true')

    def test_get_projects_slug_revisions(self):
        """Tests TimeSync.get_projects with revisions query and slug"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_projects(slug='gwm', revisions=True)

        patched_json_loader.stop()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(
            'http://ts.example.com/v1/projects/gwm?revisions=true')

    def test_get_projects_include_deleted(self):
        """Tests TimeSync.get_projects with include_deleted query"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_projects(include_deleted=True)

        patched_json_loader.stop()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(
            'http://ts.example.com/v1/projects?include_deleted=true')

    def test_get_projects_include_deleted_with_slug(self):
        """Tests TimeSync.get_projects with include_deleted query and slug,
        which is not allowed"""
        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Test that error message is returned, can't combine slug and
        # include_deleted
        self.assertEquals(ts.get_projects(slug='gwm', include_deleted=True),
                          {'pymesync error':
                           'invalid combination: slug and include_deleted'})

    def test_get_projects_include_deleted_revisions(self):
        """Tests TimeSync.get_projects with revisions and include_deleted
        queries"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_projects(revisions=True, include_deleted=True)

        patched_json_loader.stop()

        # Test that requests.get was called with correct paramaters
        requests.get.assert_called_with("http://ts.example.com/v1/projects"
                                        + "?include_deleted=true"
                                        + "&revisions=true")

    def test_get_activities(self):
        """Tests TimeSync.get_activities"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_activities()

        patched_json_loader.stop()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(
            'http://ts.example.com/v1/activities')

    def test_get_activities_slug(self):
        """Tests TimeSync.get_activities with slug"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_activities(slug='code')

        patched_json_loader.stop()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(
            'http://ts.example.com/v1/activities/code')

    def test_get_activities_revisions(self):
        """Tests TimeSync.get_activities with revisions query"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_activities(revisions=True)

        patched_json_loader.stop()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(
            'http://ts.example.com/v1/activities?revisions=true')

    def test_get_activities_slug_revisions(self):
        """Tests TimeSync.get_projects with revisions query and slug"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_activities(slug='code', revisions=True)

        patched_json_loader.stop()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(
            'http://ts.example.com/v1/activities/code?revisions=true')

    def test_get_activities_include_deleted(self):
        """Tests TimeSync.get_activities with include_deleted query"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_activities(include_deleted=True)

        patched_json_loader.stop()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(
            'http://ts.example.com/v1/activities?include_deleted=true')

    def test_get_activities_include_deleted_with_slug(self):
        """Tests TimeSync.get_activities with include_deleted query and slug,
        which is not allowed"""
        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Test that error message is returned, can't combine slug and
        # include_deleted
        self.assertEquals(ts.get_activities(slug='code', include_deleted=True),
                          {'pymesync error':
                           'invalid combination: slug and include_deleted'})

    def test_get_activities_include_deleted_revisions(self):
        """Tests TimeSync.get_activities with revisions and include_deleted
        queries"""
        # Patch json.loads - Since we mocked the API call, we won't actually be
        # getting a JSON object back, we don't want this mocked forever so just
        # patch it.
        patched_json_loader = mock.patch('json.loads')
        patched_json_loader.start()

        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_activities(revisions=True, include_deleted=True)

        patched_json_loader.stop()

        # Test that requests.get was called with correct paramaters
        requests.get.assert_called_with("http://ts.example.com/v1/activities"
                                        + "?include_deleted=true"
                                        + "&revisions=true")

    def test_json_to_python_single_object(self):
        """Test that TimeSync._json_to_python converts a json object to a python
        list of object"""
        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        json_object = '{\
            "uri": "https://code.osuosl.org/projects/ganeti-webmgr",\
            "name": "Ganeti Web Manager",\
            "slugs": ["ganeti", "gwm"],\
            "owner": "example-user",\
            "uuid": "a034806c-00db-4fe1-8de8-514575f31bfb",\
            "revision": 4,\
            "created_at": "2014-07-17",\
            "deleted_at": null,\
            "updated_at": "2014-07-20"\
        }'

        python_object = [
            {
                u'uuid': u'a034806c-00db-4fe1-8de8-514575f31bfb',
                u'updated_at': u'2014-07-20',
                u'created_at': u'2014-07-17',
                u'uri': u'https://code.osuosl.org/projects/ganeti-webmgr',
                u'name': u'Ganeti Web Manager',
                u'owner': u'example-user',
                u'deleted_at': None,
                u'slugs': [u'ganeti', u'gwm'],
                u'revision': 4
            }
        ]

        self.assertEquals(ts._json_to_python(json_object), python_object)

    def test_json_to_python_list_of_object(self):
        """Test that TimeSync._json_to_python converts a json list of objects
        to a python list of objects"""
        baseurl = 'http://ts.example.com/v1'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        json_object = '[\
            {\
                "name": "Documentation",\
                "slugs": ["docs", "doc"],\
                "uuid": "adf036f5-3d49-4a84-bef9-0sdb46380bbf",\
                "revision": 1,\
                "created_at": "2014-04-17",\
                "deleted_at": null,\
                "updated_at": null\
            },\
            {\
                "name": "Coding",\
                "slugs": ["coding", "code", "prog"],\
                "uuid": "adf036f5-3d79-4a84-bef9-062b46320bbf",\
                "revision": 1,\
                "created_at": "2014-04-17",\
                "deleted_at": null,\
                "updated_at": null\
            },\
            {\
                "name": "Research",\
                "slugs": ["research", "res"],\
                "uuid": "adf036s5-3d49-4a84-bef9-062b46380bbf",\
                "revision": 1,\
                "created_at": "2014-04-17",\
                "deleted_at": null,\
                "updated_at": null\
            }\
        ]'

        python_object = [
            {
                u'uuid': u'adf036f5-3d49-4a84-bef9-0sdb46380bbf',
                u'created_at': u'2014-04-17',
                u'updated_at': None,
                u'name': u'Documentation',
                u'deleted_at': None,
                u'slugs': [u'docs', u'doc'],
                u'revision': 1
            },
            {
                u'uuid': u'adf036f5-3d79-4a84-bef9-062b46320bbf',
                u'created_at': u'2014-04-17',
                u'updated_at': None,
                u'name': u'Coding',
                u'deleted_at': None,
                u'slugs': [u'coding', u'code', u'prog'],
                u'revision': 1
            },
            {
                u'uuid': u'adf036s5-3d49-4a84-bef9-062b46380bbf',
                u'created_at': u'2014-04-17',
                u'updated_at': None,
                u'name': u'Research',
                u'deleted_at': None,
                u'slugs': [u'research', u'res'],
                u'revision': 1
            }
        ]

        self.assertEquals(ts._json_to_python(json_object), python_object)

if __name__ == '__main__':
    unittest.main()
