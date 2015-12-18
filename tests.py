import unittest
import pymesync
import mock
from mock import patch
import requests
import json


class resp(object):

    def __init__(self):
        self.text = None
        self.status_code = None


class TestPymesync(unittest.TestCase):

    def setUp(self):
        baseurl = "http://ts.example.com/v1"
        self.ts = pymesync.TimeSync(baseurl)
        self.ts.user = "example-user"
        self.ts.password = "password"
        self.ts.auth_type = "password"
        self.ts.token = "TESTTOKEN"

    def tearDown(self):
        del(self.ts)
        requests.post = actual_post

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_create_time_valid(self, m_resp_python):
        """Tests TimeSync._create_or_update for create time with valid data"""
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

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, None, "time", "times")

        # Test it
        requests.post.assert_called_with("http://ts.example.com/v1/times",
                                         json=content)

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_time_valid(self, m_resp_python):
        """Tests TimeSync._create_or_update for update time with valid data"""
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

        # Test baseurl and uuid
        uuid = '1234-5678-90abc-d'

        # Format content for assert_called_with test
        content = {
            'auth': self.ts._token_auth(),
            'object': params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, uuid, "time", "times")

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/times/{}".format(uuid),
            json=content)

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_time_valid_less_fields(self,
                                                            m_resp_python):
        """Tests TimeSync._create_or_update for update time with one valid
        parameter"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
        }

        # Test baseurl and uuid
        uuid = '1234-5678-90abc-d'

        # Format content for assert_called_with test
        content = {
            'auth': self.ts._token_auth(),
            'object': params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, uuid, "time", "times", False)

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/times/{}".format(uuid),
            json=content)

    def test_create_or_update_create_time_invalid(self):
        """Tests TimeSync._create_or_update for create time with invalid
        field"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
            "bad": "field"
        }

        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "time", "times"),
                          [{"pymesync error":
                            "time object: invalid field: bad"}])

    def test_create_or_update_create_time_two_required_missing(self):
        """Tests TimeSync._create_or_update for create time with missing
        required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
            "user": "example-user",
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "time", "times"),
                          [{"pymesync error":
                            "time object: missing required field(s): "
                            "project, activities"}])

    def test_create_or_update_create_time_each_required_missing(self):
        """Tests TimeSync._create_or_update to create time with missing
        required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "date_worked": "2014-04-17",
        }

        params_to_test = dict(params)

        for key in params:
            del(params_to_test[key])
            self.assertEquals(self.ts._create_or_update(params_to_test, None,
                                                        "time", "times"),
                              [{"pymesync error": "time object: "
                                "missing required field(s): {}".format(key)}])
            params_to_test = dict(params)

    def test_create_or_update_create_time_type_error(self):
        """Tests TimeSync._create_or_update for create time with incorrect
        parameter types"""
        # Parameters to be sent to TimeSync
        param_list = [1, "hello", [1, 2, 3]]

        for param in param_list:
            self.assertEquals(self.ts._create_or_update(param, None,
                                                        "time", "times"),
                              [{"pymesync error":
                                "time object: must be python dictionary"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_create_time_catch_request_error(self, m):
        """Tests TimeSync._create_or_update for create time with request
        error"""
        params = {
            "duration": 12,
            "project": "ganet_web_manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        # To test that the exception is being caught with a bad baseurl,
        # we need to use the actual post method
        requests.post = actual_post

        self.assertRaises(Exception, self.ts._create_or_update(params,
                                                               None,
                                                               "time",
                                                               "times"))

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_create_user_valid(self, m_resp_python):
        """Tests TimeSync._create_or_update for create user with valid data"""
        # Parameters to be sent to TimeSync
        params = {
            "username": "example-user",
            "password": "password",
            "displayname": "Example User",
            "email": "example.user@example.com",
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, None, "user", "users")

        # Test it
        requests.post.assert_called_with("http://ts.example.com/v1/users",
                                         json=content)

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_user_valid(self, m_resp_python):
        """Tests TimeSync._create_or_update for update user with valid data"""
        # Parameters to be sent to TimeSync
        params = {
            "username": "example-user",
            "password": "password",
            "displayname": "Example User",
            "email": "example.user@example.com",
        }

        # Test baseurl and uuid
        username = "example-user"

        # Format content for assert_called_with test
        content = {
            'auth': self.ts._token_auth(),
            'object': params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, username, "user", "users", False)

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/users/{}".format(username),
            json=content)

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_user_valid_less_fields(self,
                                                            m_resp_python):
        """Tests TimeSync._create_or_update for update user with one valid
        parameter"""
        # Parameters to be sent to TimeSync
        params = {
            "displayname": "Example User",
        }

        # Test baseurl and uuid
        username = "example-user"

        # Format content for assert_called_with test
        content = {
            'auth': self.ts._token_auth(),
            'object': params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, username, "user", "users", False)

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/users/{}".format(username),
            json=content)

    def test_create_or_update_create_user_invalid(self):
        """Tests TimeSync._create_or_update for create user with invalid
        field"""
        # Parameters to be sent to TimeSync
        params = {
            "username": "example-user",
            "password": "password",
            "displayname": "Example User",
            "email": "example.user@example.com",
            "bad": "field",
        }

        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "user", "users"),
                          [{"pymesync error":
                            "time object: invalid field: bad"}])

    def test_create_or_update_create_user_two_required_missing(self):
        """Tests TimeSync._create_or_update for create user with missing
        required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "displayname": "Example User",
            "email": "example.user@example.com",
        }

        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "user", "users"),
                          [{"pymesync error":
                            "time object: missing required field(s): "
                            "username, password"}])

    def test_create_or_update_create_user_each_required_missing(self):
        """Tests TimeSync._create_or_update to create user with missing
        required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "username": "example-user",
            "password": "password",
            "displayname": "Example User",
            "email": "example.user@example.com",
        }

        params_to_test = dict(params)

        for key in params:
            del(params_to_test[key])
            self.assertEquals(self.ts._create_or_update(params_to_test, None,
                                                        "user", "users"),
                              [{"pymesync error": "user object: "
                                "missing required field(s): {}".format(key)}])
            params_to_test = dict(params)

    def test_create_or_update_create_user_type_error(self):
        """Tests TimeSync._create_or_update for create user with incorrect
        parameter types"""
        # Parameters to be sent to TimeSync
        param_list = [1, "hello", [1, 2, 3]]

        for param in param_list:
            self.assertEquals(self.ts._create_or_update(param, None,
                                                        "user", "users"),
                              [{"pymesync error":
                                "user object: must be python dictionary"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_create_user_catch_request_error(self, m):
        """Tests TimeSync._create_or_update for create user with request
        error"""
        params = {
            "username": "example-user",
            "password": "password",
            "displayname": "Example User",
            "email": "example.user@example.com",
        }

        # To test that the exception is being caught with a bad baseurl,
        # we need to use the actual post method
        requests.post = actual_post

        self.assertRaises(Exception, self.ts._create_or_update(params,
                                                               None,
                                                               "user",
                                                               "users"))

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_create_project_valid(self, m_resp_python):
        """Tests TimeSync._create_or_update for create project with valid
        data"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "owner": "example-2"
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, None, "project", "projects")

        # Test it
        requests.post.assert_called_with("http://ts.example.com/v1/projects",
                                         json=content)

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_project_valid(self, m_resp_python):
        """Tests TimeSync._create_or_update for update project with valid
        parameters"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "owner": "example-2"
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, "slug", "project", "projects")

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/projects/slug",
            json=content)

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_project_valid_less_fields(self,
                                                               m_resp_python):
        """Tests TimeSync._create_or_update for update project with one valid
        parameter"""
        # Parameters to be sent to TimeSync
        params = {
            "slugs": ["timesync", "time"],
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, "slug", "project", "projects", False)

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/projects/slug",
            json=content)

    def test_create_or_update_create_project_invalid(self):
        """Tests TimeSync._create_or_update for create project with invalid
        field"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "owner": "example-2",
            "bad": "field"
        }

        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "project", "projects"),
                          [{"pymesync error":
                            "project object: invalid field: bad"}])

    def test_create_or_update_create_project_required_missing(self):
        """Tests TimeSync._create_or_update for create project with missing
        required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
        }

        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "project", "project"),
                          [{"pymesync error": "project object: "
                            "missing required field(s): owner"}])

    def test_create_or_update_create_project_each_required_missing(self):
        """Tests TimeSync._create_or_update for create project with missing
        required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "owner": "example-2"
        }

        params_to_test = dict(params)

        for key in params:
            del(params_to_test[key])
            self.assertEquals(self.ts._create_or_update(params_to_test, None,
                                                        "project", "projects"),
                              [{"pymesync error": "project object: "
                                "missing required field(s): {}".format(key)}])
            params_to_test = dict(params)

    def test_create_or_update_create_project_type_error(self):
        """Tests TimeSync._create_or_update for create project with incorrect
        parameter types"""
        # Parameters to be sent to TimeSync
        param_list = [1, "hello", [1, 2, 3]]

        for param in param_list:
            self.assertEquals(self.ts._create_or_update(param, None,
                                                        "project", "projects"),
                              [{"pymesync error":
                                "project object: must be python dictionary"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_create_activity_valid(self, m_resp_python):
        """Tests TimeSync._create_or_update for create activity with valid
        data"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, None, "activity", "activities")

        # Test it
        requests.post.assert_called_with("http://ts.example.com/v1/activities",
                                         json=content)

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_activity_valid(self, m_resp_python):
        """Tests TimeSync._create_or_update for update activity with valid
        parameters"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, "slug", "activity", "activities")

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/activities/slug",
            json=content)

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_activity_valid_less_fields(self,
                                                                m_resp_python):
        """Tests TimeSync._create_or_update for update activity with one valid
        parameter"""
        # Parameters to be sent to TimeSync
        params = {
            "slug": "qa",
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._create_or_update(params, "slug", "activity",
                                  "activities", False)

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/activities/slug",
            json=content)

    def test_create_or_update_create_activity_invalid(self):
        """Tests TimeSync._create_or_update for create activity with invalid
        field"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
            "bad": "field",
        }

        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "activity", "activites"),
                          [{"pymesync error":
                            "activity object: invalid field: bad"}])

    def test_create_or_update_create_activity_required_missing(self):
        """Tests TimeSync._create_or_update for create activity with missing
        required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
        }

        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "activity", "activities"),
                          [{"pymesync error": "activity object: "
                            "missing required field(s): slug"}])

    def test_create_or_update_create_activity_each_required_missing(self):
        """Tests TimeSync._create_or_update for create activity with missing
        required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        params_to_test = dict(params)

        for key in params:
            del(params_to_test[key])
            self.assertEquals(self.ts._create_or_update(params_to_test,
                                                        None,
                                                        "activity",
                                                        "activities"),
                              [{"pymesync error": "activity object: "
                                "missing required field(s): {}".format(key)}])
            params_to_test = dict(params)

    def test_create_or_update_create_activity_type_error(self):
        """Tests TimeSync._create_or_update for create activity with incorrect
        parameter types"""
        # Parameters to be sent to TimeSync
        param_list = [1, "hello", [1, 2, 3]]

        for param in param_list:
            self.assertEquals(self.ts._create_or_update(param,
                                                        None,
                                                        "activity",
                                                        "activities"),
                              [{"pymesync error":
                                "activity object: must be python dictionary"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_create_time_no_auth(self, m_resp_python):
        """Tests TimeSync._create_or_update for create time with no auth"""
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

        self.ts.token = None

        # Send it
        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "time", "times"),
                          [{"pymesync error": "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_create_project_no_auth(self, m_resp_python):
        """Tests TimeSync._create_or_update for create project with no auth"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "owner": "example-2"
        }

        self.ts.token = None

        # Send it
        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "project", "projects"),
                          [{"pymesync error": "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_create_activity_no_auth(self, m_resp_python):
        """Tests TimeSync._create_or_update for create activity with no auth"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        self.ts.token = None

        # Send it
        self.assertEquals(self.ts._create_or_update(params, None,
                                                    "activity", "activities"),
                          [{"pymesync error": "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_time_no_auth(self, m_resp_python):
        """Tests TimeSync._create_or_update for update time with no auth"""
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

        self.ts.token = None

        # Send it
        self.assertEquals(self.ts._create_or_update(params, None, "time",
                                                    "times", False),
                          [{"pymesync error": "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_project_no_auth(self, m_resp_python):
        """Tests TimeSync._create_or_update for update project with no auth"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "owner": "example-2"
        }

        self.ts.token = None

        # Send it
        self.assertEquals(self.ts._create_or_update(params, None, "project",
                                                    "project", False),
                          [{"pymesync error": "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_create_or_update_update_activity_no_auth(self, m_resp_python):
        """Tests TimeSync._create_or_update for update activity with no auth"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        self.ts.token = None

        # Send it
        self.assertEquals(self.ts._create_or_update(params, None, "activity",
                                                    "activities", False),
                          [{"pymesync error": "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    def test_auth(self):
        """Tests TimeSync._auth function"""
        # Create auth block to test _auth
        auth = {"type": "password",
                "username": "example-user",
                "password": "password", }

        self.assertEquals(self.ts._auth(), auth)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_user(self, m_resp_python):
        """Tests TimeSync.get_times with username query parameter"""

        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?user=example-user&token={1}".format(self.ts.baseurl,
                                                             self.ts.token)

        # Send it
        self.ts.get_times(user=[self.ts.user])

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_proj(self, m_resp_python):
        """Tests TimeSync.get_times with project query parameter"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?project=gwm&token={1}".format(self.ts.baseurl,
                                                       self.ts.token)

        # Send it
        self.ts.get_times(project=["gwm"])

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_activity(self, m_resp_python):
        """Tests TimeSync.get_times with activity query parameter"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?activity=dev&token={1}".format(self.ts.baseurl,
                                                        self.ts.token)

        # Send it
        self.ts.get_times(activity=["dev"])

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_start_date(self, m_resp_python):
        """Tests TimeSync.get_times with start date query parameter"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?start=2015-07-23&token={1}".format(self.ts.baseurl,
                                                            self.ts.token)

        # Send it
        self.ts.get_times(start=["2015-07-23"])

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_end_date(self, m_resp_python):
        """Tests TimeSync.get_times with end date query parameter"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?end=2015-07-23&token={1}".format(self.ts.baseurl,
                                                          self.ts.token)

        # Send it
        self.ts.get_times(end=["2015-07-23"])

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_include_revisions(self, m_resp_python):
        """Tests TimeSync.get_times with include_revisions query parameter"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?include_revisions=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_times(include_revisions=True)

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_include_revisions_false(self, m_resp_python):
        """Tests TimeSync.get_times with include_revisions False query
        parameter"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?include_revisions=false&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_times(include_revisions=False)

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_include_deleted(self, m_resp_python):
        """Tests TimeSync.get_times with include_deleted query parameter"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?include_deleted=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_times(include_deleted=True)

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_include_deleted_false(self, m_resp_python):
        """Tests TimeSync.get_times with include_revisions False query
        parameter"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?include_deleted=false&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_times(include_deleted=False)

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_proj_and_activity(self, m_resp_python):
        """Tests TimeSync.get_times with project and activity query
        parameters"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?activity=dev&project=gwm&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_times(project=["gwm"], activity=["dev"])

        # Test that requests.get was called with baseurl and correct parameters
        # Multiple parameters are sorted alphabetically
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_for_activity_x3(self, m_resp_python):
        """Tests TimeSync.get_times with project and activity query
        parameters"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        token_string = "&token={}".format(self.ts.token)

        url = "{0}/times?activity=dev&activity=rev&activity=hd{1}".format(
            self.ts.baseurl, token_string)

        # Send it
        self.ts.get_times(activity=["dev", "rev", "hd"])

        # Test that requests.get was called with baseurl and correct parameters
        # Multiple parameters are sorted alphabetically
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_with_uuid(self, m_resp_python):
        """Tests TimeSync.get_times with uuid query parameter"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times/sadfasdg432?token={1}".format(self.ts.baseurl,
                                                       self.ts.token)

        # Send it
        self.ts.get_times(uuid="sadfasdg432")

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_with_uuid_and_activity(self, m_resp_python):
        """Tests TimeSync.get_times with uuid and activity query parameters"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times/sadfasdg432?token={1}".format(self.ts.baseurl,
                                                       self.ts.token)

        # Send it
        self.ts.get_times(uuid="sadfasdg432", activity=["dev"])

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_with_uuid_and_include_revisions(self, m_resp_python):
        """Tests TimeSync.get_times with uuid and include_revisions query
        parameters"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times/sadfasdg432?include_revisions=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_times(uuid="sadfasdg432", include_revisions=True)

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_with_uuid_and_include_deleted(self, m_resp_python):
        """Tests TimeSync.get_times with uuid and include_deleted query
        parameters"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times/sadfasdg432?include_deleted=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_times(uuid="sadfasdg432", include_deleted=True)

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_time_with_uuid_include_deleted_and_revisions(self,
                                                              m_resp_python):
        """Tests TimeSync.get_times with uuid and include_deleted query
        parameters"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        # Please forgive me for this. I blame the PEP8 line length rule
        endpoint = "times"
        uuid = "sadfasdg432"
        token = "token={}".format(self.ts.token)
        queries = "include_deleted=true&include_revisions=true"
        url = "{0}/{1}/{2}?{3}&{4}".format(self.ts.baseurl, endpoint, uuid,
                                           queries, token)

        # Send it
        self.ts.get_times(uuid="sadfasdg432",
                          include_revisions=True,
                          include_deleted=True)

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_all_times(self, m_resp_python):
        """Tests TimeSync.get_times with no parameters"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/times?token={1}".format(self.ts.baseurl,
                                           self.ts.token)

        # Send it
        self.ts.get_times()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(url)

    def test_get_times_bad_query(self):
        """Tests TimeSync.get_times with an invalid query parameter"""
        # Should return the error
        self.assertEquals(self.ts.get_times(bad=["query"]),
                          [{"pymesync error": "invalid query: bad"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_projects(self, m_resp_python):
        """Tests TimeSync.get_projects"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/projects?token={1}".format(self.ts.baseurl,
                                              self.ts.token)

        # Send it
        self.ts.get_projects()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_projects_slug(self, m_resp_python):
        """Tests TimeSync.get_projects with slug"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/projects/gwm?token={1}".format(self.ts.baseurl,
                                                  self.ts.token)

        # Send it
        self.ts.get_projects(slug="gwm")

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_projects_include_revisions(self, m_resp_python):
        """Tests TimeSync.get_projects with include_revisions query"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/projects?include_revisions=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_projects(include_revisions=True)

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_projects_slug_include_revisions(self, m_resp_python):
        """Tests TimeSync.get_projects with include_revisions query and slug"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/projects/gwm?include_revisions=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_projects(slug="gwm", include_revisions=True)

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_projects_include_deleted(self, m_resp_python):
        """Tests TimeSync.get_projects with include_deleted query"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/projects?include_deleted=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_projects(include_deleted=True)

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    def test_get_projects_include_deleted_with_slug(self):
        """Tests TimeSync.get_projects with include_deleted query and slug,
        which is not allowed"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        # Test that error message is returned, can't combine slug and
        # include_deleted
        self.assertEquals(self.ts.get_projects(slug="gwm",
                                               include_deleted=True),
                          [{"pymesync error":
                           "invalid combination: slug and include_deleted"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_projects_include_deleted_include_revisions(self,
                                                            m_resp_python):
        """Tests TimeSync.get_projects with include_revisions and include_deleted
        queries"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        token_string = "&token={}".format(self.ts.token)
        endpoint = "/projects"
        url = "{0}{1}?include_deleted=true&include_revisions=true{2}".format(
            self.ts.baseurl, endpoint, token_string)

        # Send it
        self.ts.get_projects(include_revisions=True, include_deleted=True)

        # Test that requests.get was called with correct parameters
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_activities(self, m_resp_python):
        """Tests TimeSync.get_activities"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/activities?token={1}".format(self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_activities()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_activities_slug(self, m_resp_python):
        """Tests TimeSync.get_activities with slug"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/activities/code?token={1}".format(self.ts.baseurl,
                                                     self.ts.token)

        # Send it
        self.ts.get_activities(slug="code")

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_activities_include_revisions(self, m_resp_python):
        """Tests TimeSync.get_activities with include_revisions query"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/activities?include_revisions=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_activities(include_revisions=True)

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_activities_slug_include_revisions(self, m_resp_python):
        """Tests TimeSync.get_projects with include_revisions query and slug"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/activities/code?include_revisions=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_activities(slug="code", include_revisions=True)

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_activities_include_deleted(self, m_resp_python):
        """Tests TimeSync.get_activities with include_deleted query"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/activities?include_deleted=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_activities(include_deleted=True)

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    def test_get_activities_include_deleted_with_slug(self):
        """Tests TimeSync.get_activities with include_deleted query and slug,
        which is not allowed"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        # Test that error message is returned, can't combine slug and
        # include_deleted
        self.assertEquals(self.ts.get_activities(slug="code",
                                                 include_deleted=True),
                          [{"pymesync error":
                           "invalid combination: slug and include_deleted"}])

    @patch("pymesync.TimeSync._response_to_python")
    def test_get_activities_include_deleted_include_revisions(self,
                                                              m_resp_python):
        """Tests TimeSync.get_activities with include_revisions and
        include_deleted queries"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        token_string = "&token={}".format(self.ts.token)
        endpoint = "/activities"
        url = "{0}{1}?include_deleted=true&include_revisions=true{2}".format(
            self.ts.baseurl, endpoint, token_string)

        # Send it
        self.ts.get_activities(include_revisions=True, include_deleted=True)

        # Test that requests.get was called with correct parameters
        requests.get.assert_called_with(url)

    def test_get_times_no_auth(self):
        """Test that get_times() returns error message when auth not set"""
        self.ts.token = None
        self.assertEquals(self.ts.get_times(),
                          [{"pymesync error":
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    def test_get_projects_no_auth(self):
        """Test that get_projects() returns error message when auth not set"""
        self.ts.token = None
        self.assertEquals(self.ts.get_projects(),
                          [{"pymesync error":
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    def test_get_activities_no_auth(self):
        """Test that get_activities() returns error message when auth not
        set"""
        self.ts.token = None
        self.assertEquals(self.ts.get_activities(),
                          [{"pymesync error":
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    def test_response_to_python_single_object(self):
        """Test that TimeSync._response_to_python converts a json object to a python
        list of object"""
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
                u"uuid": u"a034806c-00db-4fe1-8de8-514575f31bfb",
                u"updated_at": u"2014-07-20",
                u"created_at": u"2014-07-17",
                u"uri": u"https://code.osuosl.org/projects/ganeti-webmgr",
                u"name": u"Ganeti Web Manager",
                u"owner": u"example-user",
                u"deleted_at": None,
                u"slugs": [u"ganeti", u"gwm"],
                u"revision": 4
            }
        ]

        response = resp()
        response.text = json_object

        self.assertEquals(self.ts._response_to_python(response), python_object)

    def test_response_to_python_list_of_object(self):
        """Test that TimeSync._response_to_python converts a json list of objects
        to a python list of objects"""
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
                u"uuid": u"adf036f5-3d49-4a84-bef9-0sdb46380bbf",
                u"created_at": u"2014-04-17",
                u"updated_at": None,
                u"name": u"Documentation",
                u"deleted_at": None,
                u"slugs": [u"docs", u"doc"],
                u"revision": 1
            },
            {
                u"uuid": u"adf036f5-3d79-4a84-bef9-062b46320bbf",
                u"created_at": u"2014-04-17",
                u"updated_at": None,
                u"name": u"Coding",
                u"deleted_at": None,
                u"slugs": [u"coding", u"code", u"prog"],
                u"revision": 1
            },
            {
                u"uuid": u"adf036s5-3d49-4a84-bef9-062b46380bbf",
                u"created_at": u"2014-04-17",
                u"updated_at": None,
                u"name": u"Research",
                u"deleted_at": None,
                u"slugs": [u"research", u"res"],
                u"revision": 1
            }
        ]

        response = resp()
        response.text = json_object

        self.assertEquals(self.ts._response_to_python(response), python_object)

    @patch("pymesync.TimeSync._create_or_update")
    def test_create_time(self, mock_create_or_update):
        """Tests that TimeSync.create_time calls _create_or_update with correct
        parameters"""
        params = {
            "duration": 12,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.ts.create_time(params)

        mock_create_or_update.assert_called_with(params, None, "time", "times")

    @patch("pymesync.TimeSync._create_or_update")
    def test_update_time(self, mock_create_or_update):
        """Tests that TimeSync.update_time calls _create_or_update with correct
        parameters"""
        params = {
            "duration": 12,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.ts.update_time(params, "uuid")

        mock_create_or_update.assert_called_with(params, "uuid", "time",
                                                 "times", False)

    @patch("pymesync.TimeSync._create_or_update")
    def test_create_project(self, mock_create_or_update):
        """Tests that TimeSync.create_project calls _create_or_update with
        correct parameters"""
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "owner": "example-2"
        }

        self.ts.create_project(params)
        mock_create_or_update.assert_called_with(params, None,
                                                 "project", "projects")

    @patch("pymesync.TimeSync._create_or_update")
    def test_update_project(self, mock_create_or_update):
        """Tests that TimeSync.update_time calls _create_or_update with correct
        parameters"""
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "owner": "example-2"
        }

        self.ts.update_project(params, "slug")
        mock_create_or_update.assert_called_with(params, "slug", "project",
                                                 "projects", False)

    @patch("pymesync.TimeSync._create_or_update")
    def test_create_activity(self, mock_create_or_update):
        """Tests that TimeSync.create_activity calls _create_or_update with
        correct parameters"""
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        self.ts.create_activity(params)
        mock_create_or_update.assert_called_with(params, None,
                                                 "activity", "activities")

    @patch("pymesync.TimeSync._create_or_update")
    def test_update_activity(self, mock_create_or_update):
        """Tests that TimeSync.update_activity calls _create_or_update with
        correct parameters"""
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        self.ts.update_activity(params, "slug")
        mock_create_or_update.assert_called_with(params, "slug", "activity",
                                                 "activities", False)

    @patch("pymesync.TimeSync._create_or_update")
    def test_create_user(self, mock_create_or_update):
        """Tests that TimeSync.create_user calls _create_or_update with correct
        parameters"""
        params = {
            "username": "example-user",
            "password": "password",
            "displayname": "Example User",
            "email": "example.user@example.com",
        }

        self.ts.create_user(params)

        mock_create_or_update.assert_called_with(params, None, "user", "users")

    @patch("pymesync.TimeSync._create_or_update")
    def test_update_user(self, mock_create_or_update):
        """Tests that TimeSync.update_user calls _create_or_update with correct
        parameters"""
        params = {
            "username": "example-user",
            "password": "password",
            "displayname": "Example User",
            "email": "example.user@example.com",
        }

        self.ts.update_user(params, "example")
        mock_create_or_update.assert_called_with(params, "example", "user",
                                                 "users", False)

    @patch("pymesync.TimeSync._response_to_python")
    def test_authentication(self, mock_response_to_python):
        """Tests authenticate method for url and data construction"""
        auth = {
            "auth": {
                "type": "password",
                "username": "example-user",
                "password": "password"
            }
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        self.ts.authenticate("example-user", "password", "password")

        requests.post.assert_called_with("http://ts.example.com/v1/login",
                                         json=auth)

    def test_authentication_return_success(self):
        """Tests authenticate method with a token return"""
        # Use this fake response object for mocking requests.post
        response = resp()
        response.text = json.dumps({"token": "sometoken"})

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post,
                                             return_value=response)

        auth_block = self.ts.authenticate("example-user",
                                          "password",
                                          "password")

        self.assertEquals(auth_block[0]["token"], self.ts.token, "sometoken")
        self.assertEquals(auth_block, [{"token": "sometoken"}])

    def test_authentication_return_error(self):
        """Tests authenticate method with an error return"""
        # Use this fake response object for mocking requests.post
        response = resp()
        response.text = json.dumps({"status": 401,
                                    "error": "Authentication failure",
                                    "text": "Invalid username or password"})

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post,
                                             return_value=response)

        auth_block = self.ts.authenticate("example-user",
                                          "password",
                                          "password")

        self.assertEquals(auth_block, [{"status": 401,
                                        "error": "Authentication failure",
                                        "text": "Invalid username or "
                                        "password"}])

    def test_authentication_no_username(self):
        """Tests authenticate method with no username in call"""
        self.assertEquals(self.ts.authenticate(password="password",
                                               auth_type="password"),
                          [{"pymesync error": "Missing username; "
                            "please add to method call"}])

    def test_authentication_no_password(self):
        """Tests authenticate method with no password in call"""
        self.assertEquals(self.ts.authenticate(username="username",
                                               auth_type="password"),
                          [{"pymesync error": "Missing password; "
                            "please add to method call"}])

    def test_authentication_no_auth_type(self):
        """Tests authenticate method with no auth_type in call"""
        self.assertEquals(self.ts.authenticate(password="password",
                                               username="username"),
                          [{"pymesync error": "Missing auth_type; "
                            "please add to method call"}])

    def test_authentication_no_username_or_password(self):
        """Tests authenticate method with no username or password in call"""
        self.assertEquals(self.ts.authenticate(auth_type="password"),
                          [{"pymesync error": "Missing username, password; "
                            "please add to method call"}])

    def test_authentication_no_username_or_auth_type(self):
        """Tests authenticate method with no username or auth_type in call"""
        self.assertEquals(self.ts.authenticate(password="password"),
                          [{"pymesync error": "Missing username, auth_type; "
                            "please add to method call"}])

    def test_authentication_no_password_or_auth_type(self):
        """Tests authenticate method with no username or auth_type in call"""
        self.assertEquals(self.ts.authenticate(username="username"),
                          [{"pymesync error": "Missing password, auth_type; "
                            "please add to method call"}])

    def test_authentication_no_arguments(self):
        """Tests authenticate method with no arguments in call"""
        self.assertEquals(self.ts.authenticate(),
                          [{"pymesync error": "Missing username, password, "
                            "auth_type; please add to method call"}])

    def test_authentication_no_token_in_response(self):
        """Tests authenticate method with no token in response"""
        response = resp()
        response.status_code = 502

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post,
                                             return_value=response)

        self.assertEquals(self.ts.authenticate(username="username",
                                               password="password",
                                               auth_type="password"),
                          [{"pymesync error":
                            "connection to TimeSync failed at baseurl "
                            "http://ts.example.com/v1 - "
                            "response status was 502"}])

    def test_local_auth_error_with_token(self):
        """Test internal local_auth_error method with token"""
        self.assertIsNone(self.ts._local_auth_error())

    def test_local_auth_error_no_token(self):
        """Test internal local_auth_error method with no token"""
        self.ts.token = None
        self.assertEquals(self.ts._local_auth_error(),
                          "Not authenticated with TimeSync, "
                          "call self.authenticate() first")

    def test_handle_other_connection_response(self):
        """Test that pymesync doesn't break when getting a response that is
        not a JSON object"""
        response = resp()
        response.status_code = 502

        self.assertEquals(self.ts._response_to_python(response),
                          [{"pymesync error":
                            "connection to TimeSync failed at baseurl "
                            "http://ts.example.com/v1 - "
                            "response status was 502"}])

if __name__ == "__main__":
    actual_post = requests.post  # Save this for testing exceptions
    unittest.main()
