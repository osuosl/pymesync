import unittest
import pymesync
import mock
from mock import patch
import requests
import json
import base64
import ast
import time


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
        requests.delete = actual_delete

    def test_instantiate_with_token(self):
        """Test that instantiating pymesync with a token sets the token
        variable"""
        ts = pymesync.TimeSync("baseurl", token="TOKENTOCHECK")
        self.assertEquals(ts.token, "TOKENTOCHECK")

    def test_instantiate_without_token(self):
        """Test that instantiating pymesync without a token does not se the
        token variable"""
        ts = pymesync.TimeSync("baseurl")
        self.assertIsNone(ts.token)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_create_time_valid(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for create time with
        valid data"""
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
            "auth": self.ts._TimeSync__token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, None, "time", "times")

        # Test it
        requests.post.assert_called_with("http://ts.example.com/v1/times",
                                         json=content)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_time_valid(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update time with
        valid data"""
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
            'auth': self.ts._TimeSync__token_auth(),
            'object': params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, uuid, "time", "times")

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/times/{}".format(uuid),
            json=content)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_time_valid_less_fields(self,
                                                            m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update time with one
        valid parameter"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
        }

        # Test baseurl and uuid
        uuid = '1234-5678-90abc-d'

        # Format content for assert_called_with test
        content = {
            'auth': self.ts._TimeSync__token_auth(),
            'object': params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, uuid, "time",
                                            "times", False)

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/times/{}".format(uuid),
            json=content)

    def test_create_or_update_create_time_invalid(self):
        """Tests TimeSync._TimeSync__create_or_update for create time with
        invalid field"""
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

        self.assertEquals(self.ts._TimeSync__create_or_update(params, None,
                                                              "time", "times"),
                          [{self.ts.error:
                            "time object: invalid field: bad"}])

    def test_create_or_update_create_time_two_required_missing(self):
        """Tests TimeSync._TimeSync__create_or_update for create time with
        missing required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
            "user": "example-user",
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts._TimeSync__create_or_update(params, None,
                                                              "time", "times"),
                          [{self.ts.error:
                            "time object: missing required field(s): "
                            "project, activities"}])

    def test_create_or_update_create_time_each_required_missing(self):
        """Tests TimeSync._TimeSync__create_or_update to create time with
        missing required fields"""
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
            self.assertEquals(self.ts._TimeSync__create_or_update(
                              params_to_test, None, "time", "times"),
                              [{self.ts.error: "time object: "
                                "missing required field(s): {}".format(key)}])
            params_to_test = dict(params)

    def test_create_or_update_create_time_type_error(self):
        """Tests TimeSync._TimeSync__create_or_update for create time with
        incorrect parameter types"""
        # Parameters to be sent to TimeSync
        param_list = [1, "hello", [1, 2, 3], None, True, False, 1.234]

        for param in param_list:
            self.assertEquals(self.ts._TimeSync__create_or_update(param,
                                                                  None,
                                                                  "time",
                                                                  "times"),
                              [{self.ts.error:
                                "time object: must be python dictionary"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_create_time_catch_request_error(self, m):
        """Tests TimeSync._TimeSync__create_or_update for create time with
        request error"""
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

        self.assertRaises(Exception, self.ts._TimeSync__create_or_update(
            params, None, "time", "times"))

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_create_user_valid(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for create user with
        valid data"""
        # Parameters to be sent to TimeSync
        params = {
            "username": "example-user",
            "password": "password",
            "displayname": "Example User",
            "email": "example.user@example.com",
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._TimeSync__token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, None, "user", "users")

        # Test it
        requests.post.assert_called_with("http://ts.example.com/v1/users",
                                         json=content)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_user_valid(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update user with
        valid data"""
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
            'auth': self.ts._TimeSync__token_auth(),
            'object': params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, username, "user",
                                            "users", False)

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/users/{}".format(username),
            json=content)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_user_valid_less_fields(self,
                                                            m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update user with one valid
        parameter"""
        # Parameters to be sent to TimeSync
        params = {
            "displayname": "Example User",
        }

        # Test baseurl and uuid
        username = "example-user"

        # Format content for assert_called_with test
        content = {
            'auth': self.ts._TimeSync__token_auth(),
            'object': params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, username, "user",
                                            "users", False)

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/users/{}".format(username),
            json=content)

    def test_create_or_update_create_user_invalid(self):
        """Tests TimeSync._TimeSync__create_or_update for create user with invalid
        field"""
        # Parameters to be sent to TimeSync
        params = {
            "username": "example-user",
            "password": "password",
            "displayname": "Example User",
            "email": "example.user@example.com",
            "bad": "field",
        }

        self.assertEquals(self.ts._TimeSync__create_or_update(params, None,
                                                              "user", "users"),
                          [{self.ts.error:
                            "user object: invalid field: bad"}])

    def test_create_or_update_create_user_two_required_missing(self):
        """Tests TimeSync._TimeSync__create_or_update for create user with missing
        required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "displayname": "Example User",
            "email": "example.user@example.com",
        }

        self.assertEquals(self.ts._TimeSync__create_or_update(params, None,
                                                              "user", "users"),
                          [{self.ts.error:
                            "user object: missing required field(s): "
                            "username, password"}])

    def test_create_or_update_create_user_each_required_missing(self):
        """Tests TimeSync._TimeSync__create_or_update to create user with
        missing required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "username": "example-user",
            "password": "password",
        }

        params_to_test = dict(params)

        for key in params:
            del(params_to_test[key])
            self.assertEquals(self.ts._TimeSync__create_or_update(
                              params_to_test, None, "user", "users"),
                              [{self.ts.error: "user object: "
                                "missing required field(s): {}".format(key)}])
            params_to_test = dict(params)

    def test_create_or_update_create_user_type_error(self):
        """Tests TimeSync._TimeSync__create_or_update for create user with incorrect
        parameter types"""
        # Parameters to be sent to TimeSync
        param_list = [1, "hello", [1, 2, 3], None, True, False, 1.234]

        for param in param_list:
            self.assertEquals(self.ts._TimeSync__create_or_update(param,
                                                                  None,
                                                                  "user",
                                                                  "users"),
                              [{self.ts.error:
                                "user object: must be python dictionary"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_create_user_catch_request_error(self, m):
        """Tests TimeSync._TimeSync__create_or_update for create user with
        request error"""
        params = {
            "username": "example-user",
            "password": "password",
            "displayname": "Example User",
            "email": "example.user@example.com",
        }

        # To test that the exception is being caught with a bad baseurl,
        # we need to use the actual post method
        requests.post = actual_post

        self.assertRaises(Exception, self.ts._TimeSync__create_or_update(
                          params, None, "user", "users"))

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_create_project_valid(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for create project with
        valid data"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._TimeSync__token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, None,
                                            "project", "projects")

        # Test it
        requests.post.assert_called_with("http://ts.example.com/v1/projects",
                                         json=content)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_project_valid(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update project with
        valid parameters"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._TimeSync__token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, "slug",
                                            "project", "projects")

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/projects/slug",
            json=content)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_project_valid_less_fields(self,
                                                               m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update project with
        one valid parameter"""
        # Parameters to be sent to TimeSync
        params = {
            "slugs": ["timesync", "time"],
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._TimeSync__token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, "slug", "project",
                                            "projects", False)

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/projects/slug",
            json=content)

    def test_create_or_update_create_project_invalid(self):
        """Tests TimeSync._TimeSync__create_or_update for create project with
        invalid field"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "bad": "field"
        }

        self.assertEquals(self.ts._TimeSync__create_or_update(params,
                                                              None,
                                                              "project",
                                                              "projects"),
                          [{self.ts.error:
                            "project object: invalid field: bad"}])

    def test_create_or_update_create_project_required_missing(self):
        """Tests TimeSync._TimeSync__create_or_update for create project with
        missing required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "slugs": ["timesync", "time"],
        }

        self.assertEquals(self.ts._TimeSync__create_or_update(params,
                                                              None,
                                                              "project",
                                                              "project"),
                          [{self.ts.error: "project object: "
                            "missing required field(s): name"}])

    def test_create_or_update_create_project_each_required_missing(self):
        """Tests TimeSync._TimeSync__create_or_update for create project with
        missing required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
        }

        params_to_test = dict(params)

        for key in params:
            del(params_to_test[key])
            self.assertEquals(self.ts._TimeSync__create_or_update(
                              params_to_test, None, "project", "projects"),
                              [{self.ts.error: "project object: "
                                "missing required field(s): {}".format(key)}])
            params_to_test = dict(params)

    def test_create_or_update_create_project_type_error(self):
        """Tests TimeSync._TimeSync__create_or_update for create project with
        incorrect parameter types"""
        # Parameters to be sent to TimeSync
        param_list = [1, "hello", [1, 2, 3], None, True, False, 1.234]

        for param in param_list:
            self.assertEquals(self.ts._TimeSync__create_or_update(param,
                                                                  None,
                                                                  "project",
                                                                  "projects"),
                              [{self.ts.error:
                                "project object: must be python dictionary"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_create_activity_valid(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        valid data"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._TimeSync__token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, None,
                                            "activity", "activities")

        # Test it
        requests.post.assert_called_with("http://ts.example.com/v1/activities",
                                         json=content)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_activity_valid(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update activity with
        valid parameters"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._TimeSync__token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, "slug",
                                            "activity", "activities")

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/activities/slug",
            json=content)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_activity_valid_less_fields(self,
                                                                m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update activity with
        one valid parameter"""
        # Parameters to be sent to TimeSync
        params = {
            "slug": "qa",
        }

        # Format content for assert_called_with test
        content = {
            "auth": self.ts._TimeSync__token_auth(),
            "object": params,
        }

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        self.ts._TimeSync__create_or_update(params, "slug", "activity",
                                            "activities", False)

        # Test it
        requests.post.assert_called_with(
            "http://ts.example.com/v1/activities/slug",
            json=content)

    def test_create_or_update_create_activity_invalid(self):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        invalid field"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
            "bad": "field",
        }

        self.assertEquals(self.ts._TimeSync__create_or_update(params,
                                                              None,
                                                              "activity",
                                                              "activites"),
                          [{self.ts.error:
                            "activity object: invalid field: bad"}])

    def test_create_or_update_create_activity_required_missing(self):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        missing required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
        }

        self.assertEquals(self.ts._TimeSync__create_or_update(params,
                                                              None,
                                                              "activity",
                                                              "activities"),
                          [{self.ts.error: "activity object: "
                            "missing required field(s): slug"}])

    def test_create_or_update_create_activity_each_required_missing(self):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        missing required fields"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        params_to_test = dict(params)

        for key in params:
            del(params_to_test[key])
            self.assertEquals(self.ts._TimeSync__create_or_update(
                              params_to_test, None, "activity", "activities"),
                              [{self.ts.error: "activity object: "
                                "missing required field(s): {}".format(key)}])
            params_to_test = dict(params)

    def test_create_or_update_create_activity_type_error(self):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        incorrect parameter types"""
        # Parameters to be sent to TimeSync
        param_list = [1, "hello", [1, 2, 3], None, True, False, 1.234]

        for param in param_list:
            self.assertEquals(self.ts._TimeSync__create_or_update(param,
                              None, "activity", "activities"),
                              [{self.ts.error:
                                "activity object: must be python dictionary"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_create_time_no_auth(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for create time with no
        auth"""
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
        self.assertEquals(self.ts._TimeSync__create_or_update(params, None,
                                                              "time", "times"),
                          [{self.ts.error: "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_create_project_no_auth(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for create project with no
        auth"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
        }

        self.ts.token = None

        # Send it
        self.assertEquals(self.ts._TimeSync__create_or_update(params,
                                                              None,
                                                              "project",
                                                              "projects"),
                          [{self.ts.error: "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_create_activity_no_auth(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        no auth"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        self.ts.token = None

        # Send it
        self.assertEquals(self.ts._TimeSync__create_or_update(params,
                                                              None,
                                                              "activity",
                                                              "activities"),
                          [{self.ts.error: "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_time_no_auth(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update time with no
        auth"""
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
        self.assertEquals(self.ts._TimeSync__create_or_update(params,
                                                              None,
                                                              "time",
                                                              "times",
                                                              False),
                          [{self.ts.error: "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_project_no_auth(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update project with
        no auth"""
        # Parameters to be sent to TimeSync
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
        }

        self.ts.token = None

        # Send it
        self.assertEquals(self.ts._TimeSync__create_or_update(params,
                                                              None,
                                                              "project",
                                                              "project",
                                                              False),
                          [{self.ts.error: "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_create_or_update_update_activity_no_auth(self, m_resp_python):
        """Tests TimeSync._TimeSync__create_or_update for update activity with
        no auth"""
        # Parameters to be sent to TimeSync
        params = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        self.ts.token = None

        # Send it
        self.assertEquals(self.ts._TimeSync__create_or_update(params,
                                                              None,
                                                              "activity",
                                                              "activities",
                                                              False),
                          [{self.ts.error: "Not authenticated with "
                            "TimeSync, call self.authenticate() first"}])

    def test_auth(self):
        """Tests TimeSync._TimeSync__auth function"""
        # Create auth block to test _auth
        auth = {"type": "password",
                "username": "example-user",
                "password": "password", }

        self.assertEquals(self.ts._TimeSync__auth(), auth)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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
                          [{self.ts.error: "invalid query: bad"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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
                          [{self.ts.error:
                           "invalid combination: slug and include_deleted"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_get_activities(self, m_resp_python):
        """Tests TimeSync.get_activities"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/activities?token={1}".format(self.ts.baseurl, self.ts.token)

        # Send it
        self.ts.get_activities()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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
                          [{self.ts.error:
                           "invalid combination: slug and include_deleted"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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
                          [{self.ts.error:
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    def test_get_projects_no_auth(self):
        """Test that get_projects() returns error message when auth not set"""
        self.ts.token = None
        self.assertEquals(self.ts.get_projects(),
                          [{self.ts.error:
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    def test_get_activities_no_auth(self):
        """Test that get_activities() returns error message when auth not
        set"""
        self.ts.token = None
        self.assertEquals(self.ts.get_activities(),
                          [{self.ts.error:
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_get_users(self, m_resp_python):
        """Tests TimeSync.get_users"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{}/users".format(self.ts.baseurl)

        # Send it
        self.ts.get_users()

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_get_users_username(self, m_resp_python):
        """Tests TimeSync.get_users with username"""
        # Mock requests.get
        requests.get = mock.Mock("requests.get")

        url = "{0}/users/{1}".format(self.ts.baseurl, "example-user")

        # Send it
        self.ts.get_users("example-user")

        # Test that requests.get was called correctly
        requests.get.assert_called_with(url)

    def test_get_users_no_auth(self):
        """Test that get_users() returns error message when auth not set"""
        self.ts.token = None
        self.assertEquals(self.ts.get_users(),
                          [{self.ts.error:
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    def test_response_to_python_single_object(self):
        """Test that TimeSync._TimeSync__response_to_python converts a json
        object to a python list of object"""
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

        self.assertEquals(self.ts._TimeSync__response_to_python(response),
                          python_object)

    def test_response_to_python_list_of_object(self):
        """Test that TimeSync._TimeSync__response_to_python converts a json
        list of objects to a python list of objects"""
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

        self.assertEquals(self.ts._TimeSync__response_to_python(response),
                          python_object)

    def test_response_to_python_empty_response(self):
        """Check that __response_to_python returns correctly for delete_*
        methods"""
        response = resp()
        response.text = ""
        response.status_code = 200
        self.assertEquals(self.ts._TimeSync__response_to_python(response),
                          [{"status": 200}])

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
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

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
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

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_create_project(self, mock_create_or_update):
        """Tests that TimeSync.create_project calls _create_or_update with
        correct parameters"""
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
        }

        self.ts.create_project(params)
        mock_create_or_update.assert_called_with(params, None,
                                                 "project", "projects")

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_update_project(self, mock_create_or_update):
        """Tests that TimeSync.update_time calls _create_or_update with correct
        parameters"""
        params = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
        }

        self.ts.update_project(params, "slug")
        mock_create_or_update.assert_called_with(params, "slug", "project",
                                                 "projects", False)

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
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

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
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

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
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

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
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

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
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
                          [{self.ts.error: "Missing username; "
                            "please add to method call"}])

    def test_authentication_no_password(self):
        """Tests authenticate method with no password in call"""
        self.assertEquals(self.ts.authenticate(username="username",
                                               auth_type="password"),
                          [{self.ts.error: "Missing password; "
                            "please add to method call"}])

    def test_authentication_no_auth_type(self):
        """Tests authenticate method with no auth_type in call"""
        self.assertEquals(self.ts.authenticate(password="password",
                                               username="username"),
                          [{self.ts.error: "Missing auth_type; "
                            "please add to method call"}])

    def test_authentication_no_username_or_password(self):
        """Tests authenticate method with no username or password in call"""
        self.assertEquals(self.ts.authenticate(auth_type="password"),
                          [{self.ts.error: "Missing username, password; "
                            "please add to method call"}])

    def test_authentication_no_username_or_auth_type(self):
        """Tests authenticate method with no username or auth_type in call"""
        self.assertEquals(self.ts.authenticate(password="password"),
                          [{self.ts.error: "Missing username, auth_type; "
                            "please add to method call"}])

    def test_authentication_no_password_or_auth_type(self):
        """Tests authenticate method with no username or auth_type in call"""
        self.assertEquals(self.ts.authenticate(username="username"),
                          [{self.ts.error: "Missing password, auth_type; "
                            "please add to method call"}])

    def test_authentication_no_arguments(self):
        """Tests authenticate method with no arguments in call"""
        self.assertEquals(self.ts.authenticate(),
                          [{self.ts.error: "Missing username, password, "
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
                          [{self.ts.error:
                            "connection to TimeSync failed at baseurl "
                            "http://ts.example.com/v1 - "
                            "response status was 502"}])

    def test_local_auth_error_with_token(self):
        """Test internal local_auth_error method with token"""
        self.assertIsNone(self.ts._TimeSync__local_auth_error())

    def test_local_auth_error_no_token(self):
        """Test internal local_auth_error method with no token"""
        self.ts.token = None
        self.assertEquals(self.ts._TimeSync__local_auth_error(),
                          "Not authenticated with TimeSync, "
                          "call self.authenticate() first")

    def test_handle_other_connection_response(self):
        """Test that pymesync doesn't break when getting a response that is
        not a JSON object"""
        response = resp()
        response.status_code = 502

        self.assertEquals(self.ts._TimeSync__response_to_python(response),
                          [{self.ts.error:
                            "connection to TimeSync failed at baseurl "
                            "http://ts.example.com/v1 - "
                            "response status was 502"}])

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_delete_object_time(self, m_resp_python):
        """Test that _delete_object calls requests.delete with the correct
        url"""
        requests.delete = mock.create_autospec(requests.delete)
        url = "{0}/times/abcd-3453-3de3-99sh?token={1}".format(self.ts.baseurl,
                                                               self.ts.token)
        self.ts._TimeSync__delete_object("times", "abcd-3453-3de3-99sh")
        requests.delete.assert_called_with(url)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_delete_object_project(self, m_resp_python):
        """Test that _delete_object calls requests.delete with the correct
        url"""
        requests.delete = mock.create_autospec(requests.delete)
        url = "{0}/projects/ts?token={1}".format(self.ts.baseurl,
                                                 self.ts.token)
        self.ts._TimeSync__delete_object("projects", "ts")
        requests.delete.assert_called_with(url)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_delete_object_activity(self, m_resp_python):
        """Test that _delete_object calls requests.delete with the correct
        url"""
        requests.delete = mock.create_autospec(requests.delete)
        url = "{0}/activities/code?token={1}".format(self.ts.baseurl,
                                                     self.ts.token)
        self.ts._TimeSync__delete_object("activities", "code")
        requests.delete.assert_called_with(url)

    @patch("pymesync.TimeSync._TimeSync__response_to_python")
    def test_delete_object_user(self, m_resp_python):
        """Test that _delete_object calls requests.delete with the correct
        url"""
        requests.delete = mock.create_autospec(requests.delete)
        url = "{0}/users/example-user?token={1}".format(self.ts.baseurl,
                                                        self.ts.token)
        self.ts._TimeSync__delete_object("users", "example-user")
        requests.delete.assert_called_with(url)

    @patch("pymesync.TimeSync._TimeSync__delete_object")
    def test_delete_time(self, m_delete_object):
        """Test that delete_time calls internal function correctly"""
        self.ts.delete_time("abcd-3453-3de3-99sh")
        m_delete_object.assert_called_with("times", "abcd-3453-3de3-99sh")

    def test_delete_time_no_auth(self):
        """Test that delete_time returns proper error on authentication
        failure"""
        self.ts.token = None
        self.assertEquals(self.ts.delete_time("abcd-3453-3de3-99sh"),
                          [{"pymesync error":
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    def test_delete_time_no_uuid(self):
        """Test that delete_time returns proper error when uuid not provided"""
        self.assertEquals(self.ts.delete_time(),
                          [{"pymesync error":
                            "missing uuid; please add to method call"}])

    @patch("pymesync.TimeSync._TimeSync__delete_object")
    def test_delete_project(self, m_delete_object):
        """Test that delete_project calls internal function correctly"""
        self.ts.delete_project("ts")
        m_delete_object.assert_called_with("projects", "ts")

    def test_delete_project_no_auth(self):
        """Test that delete_project returns proper error on authentication
        failure"""
        self.ts.token = None
        self.assertEquals(self.ts.delete_project("ts"),
                          [{"pymesync error":
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    def test_delete_project_no_slug(self):
        """Test that delete_project returns proper error when slug not
        provided"""
        self.assertEquals(self.ts.delete_project(),
                          [{"pymesync error":
                            "missing slug; please add to method call"}])

    @patch("pymesync.TimeSync._TimeSync__delete_object")
    def test_delete_activity(self, m_delete_object):
        """Test that delete_activity calls internal function correctly"""
        self.ts.delete_activity("code")
        m_delete_object.assert_called_with("activities", "code")

    def test_delete_activity_no_auth(self):
        """Test that delete_activity returns proper error on authentication
        failure"""
        self.ts.token = None
        self.assertEquals(self.ts.delete_activity("code"),
                          [{"pymesync error":
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    def test_delete_activity_no_slug(self):
        """Test that delete_activity returns proper error when slug not
        provided"""
        self.assertEquals(self.ts.delete_activity(),
                          [{"pymesync error":
                            "missing slug; please add to method call"}])

    @patch("pymesync.TimeSync._TimeSync__delete_object")
    def test_delete_user(self, m_delete_object):
        """Test that delete_user calls internal function correctly"""
        self.ts.delete_user("example-user")
        m_delete_object.assert_called_with("users", "example-user")

    def test_delete_user_no_auth(self):
        """Test that delete_user returns proper error on authentication
        failure"""
        self.ts.token = None
        self.assertEquals(self.ts.delete_user("example-user"),
                          [{"pymesync error":
                            "Not authenticated with TimeSync, "
                            "call self.authenticate() first"}])

    def test_delete_user_no_username(self):
        """Test that delete_user returns proper error when username not
        provided"""
        self.assertEquals(self.ts.delete_user(),
                          [{"pymesync error":
                            "missing username; please add to method call"}])

    def test_token_expiration_valid(self):
        """Test that token_expiration_time returns valid date from a valid
        token"""
        self.ts.token = ("eyJ0eXAiOiJKV1QiLCJhbGciOiJITUFDLVNIQTUxMiJ9.eyJpc3M"
                         "iOiJvc3Vvc2wtdGltZXN5bmMtc3RhZ2luZyIsInN1YiI6InRlc3Q"
                         "iLCJleHAiOjE0NTI3MTQzMzQwODcsImlhdCI6MTQ1MjcxMjUzNDA"
                         "4N30=.QP2FbiY3I6e2eN436hpdjoBFbW9NdrRUHbkJ+wr9GK9mMW"
                         "7/oC/oKnutCwwzMCwjzEx6hlxnGo6/LiGyPBcm3w==")

        decoded_payload = base64.b64decode(self.ts.token).split("}", 1)[1]
        exp_int = ast.literal_eval(decoded_payload)['exp'] / 1000
        exp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(exp_int))

        self.assertEquals(self.ts.token_expiration_time(),
                          [{'expiration': exp_str}])

    def test_token_expiration_invalid(self):
        """Test that token_expiration_time returns correct from an invalid
        token"""
        self.assertEquals(self.ts.token_expiration_time(),
                          [{self.ts.error: "improperly encoded token"}])

    def test_token_expiration_no_auth(self):
        """Test that token_expiration_time returns correct error when user is
        not authenticated"""
        self.ts.token = None
        self.assertEquals(self.ts.token_expiration_time(),
                          [{self.ts.error: "Not authenticated with TimeSync, "
                                           "call self.authenticate() first"}])


if __name__ == "__main__":
    actual_post = requests.post  # Save this for testing exceptions
    actual_delete = requests.delete
    unittest.main()
