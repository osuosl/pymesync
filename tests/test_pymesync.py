import unittest
import pymesync
import mock
from mock import patch
import json
import base64
import ast
import datetime
import bcrypt

import test_data


class resp(object):

    def __init__(self):
        self.text = None
        self.status_code = None


class pymesync_test():

    def __init__(self, data, patch_names=[]):
        self.data_in = data.data_in
        self.data_out = data.data_out
        self.patch_names = patch_names

    def __call__(self, test):
        def wrapped_test(testcase):
            patchers = []
            mocks = []
            for patch_name in self.patch_names:
                patcher = patch(patch_name)
                
                mocks.append(patcher.start())
                patchers.append(patcher)

            try:
                test(testcase, self.data_in, self.data_out, *mocks)
            finally:
                for patcher in patchers:
                    patcher.stop()

        return wrapped_test


class TestPymesync(unittest.TestCase):

    def setUp(self):
        baseurl = "http://ts.example.com/v1"
        self.ts = pymesync.TimeSync(baseurl)
        self.ts.user = "example-user"
        self.ts.password = "password"
        self.ts.auth_type = "password"
        self.ts.token = "TESTTOKEN"

        requests_patcher = patch("pymesync.pymesync.requests")
        self.mock_requests = requests_patcher.start()

        self.addCleanup(requests_patcher.stop)

    def test_instantiate_with_token(self):
        """Test that instantiating pymesync with a token sets the token
        variable"""
        ts = pymesync.TimeSync("baseurl", token="TOKENTOCHECK")
        assert ts.token == "TOKENTOCHECK"

    def test_instantiate_without_token(self):
        """Test that instantiating pymesync without a token does not set the
        token variable"""
        ts = pymesync.TimeSync("baseurl")
        assert ts.token is None

    @pymesync_test(test_data.create_or_update_create_time_valid_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_create_time_valid(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for create time with
        valid data"""
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_update_time_valid_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_update_time_valid(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for update time with
        valid data"""
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_update_time_valid_less_fields_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_update_time_valid_less_fields(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for update time with one
        valid parameter"""
        # Send it
        print self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_create_time_invalid_data)
    def test_create_or_update_create_time_invalid(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create time with
        invalid field"""
        expected = { self.ts.error: "time object: invalid field: bad" }

        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_time_two_required_missing_data)
    def test_create_or_update_create_time_two_required_missing(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create time with
        missing required fields"""
        expected = { self.ts.error: "time object: missing required field(s): "
                                    "duration, project"}

        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_time_each_required_missing_data)
    def test_create_or_update_create_time_each_required_missing(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update to create time with
        missing required fields"""
        time = data_in[0]

        time_to_test = dict(time)

        for key in time:
            del(time_to_test[key])

            expected = {self.ts.error: "time object: missing required "
                                       "field(s): {}".format(key)}

            ts_parameters = [time_to_test] + data_in[1:]

            result = self.ts._TimeSync__create_or_update(*ts_parameters)

            assert result == expected

            time_to_test = dict(time)

    @pymesync_test(test_data.create_or_update_create_time_type_error_data)
    def test_create_or_update_create_time_type_error(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create time with
        incorrect parameter types"""
        expected = {self.ts.error: "time object: must be python dictionary"}

        for param in data_in[0]:
            ts_parameters = [param] + data_in[1:]

            result = self.ts._TimeSync__create_or_update(*ts_parameters)

            assert result == expected

    @pymesync_test(test_data.create_or_update_create_user_valid_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_create_user_valid(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for create user with
        valid data"""
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_update_user_valid_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_update_user_valid(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for update user with
        valid data"""
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_update_user_valid_less_fields_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_update_user_valid_less_fields(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for update user with one
        valid parameter"""
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_create_user_invalid_data)
    def test_create_or_update_create_user_invalid(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create user with invalid
        field"""
        expected = {self.ts.error: "user object: invalid field: bad"}

        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_user_two_required_missing_data)
    def test_create_or_update_create_user_two_required_missing(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create user with missing
        required fields"""
        expected = {self.ts.error: "user object: missing required field(s): "
                                   "username, password"}

        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_user_each_required_missing_data)
    def test_create_or_update_create_user_each_required_missing(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update to create user with
        missing required fields"""
        user = data_in[0]

        user_to_test = dict(user)

        for key in user:
            del(user_to_test[key])

            expected = {self.ts.error: "user object: missing required "
                                       "field(s): {}".format(key)}

            ts_parameters = [user_to_test] + data_in[1:]

            result = self.ts._TimeSync__create_or_update(*ts_parameters)

            assert result == expected

            user_to_test = dict(user)

    @pymesync_test(test_data.create_or_update_create_user_type_error_data)
    def test_create_or_update_create_user_type_error(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create user with incorrect
        parameter types"""
        expected = {self.ts.error: "user object: must be python dictionary"}

        for param in data_in[0]:
            ts_parameters = [param] + data_in[1:]

            result = self.ts._TimeSync__create_or_update(*ts_parameters)

            assert result == expected

    @pymesync_test(test_data.create_or_update_create_project_valid_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_create_project_valid(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for create project with
        valid data"""
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_update_project_valid_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_update_project_valid(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for update project with
        valid parameters"""
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_update_project_valid_less_fields_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_update_project_valid_less_fields(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for update project with
        one valid parameter"""
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_create_project_invalid_data)
    def test_create_or_update_create_project_invalid(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create project with
        invalid field"""
        expected = {self.ts.error: "project object: invalid field: bad"}

        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_project_required_missing_data)
    def test_create_or_update_create_project_required_missing(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create project with
        missing required fields"""
        expected = {self.ts.error: "project object: missing required "
                                   "field(s): name"}

        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_project_each_required_missing_data)
    def test_create_or_update_create_project_each_required_missing(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create project with
        missing required fields"""
        project = dict(data_in[0])

        for key in data_in[0]:
            del(project[key])

            expected = {self.ts.error: "project object: missing required "
                                       "field(s): {}".format(key)}

            ts_parameters = [project] + data_in[1:]

            result = self.ts._TimeSync__create_or_update(*ts_parameters)

            assert result == expected

            project = dict(data_in[0])

    @pymesync_test(test_data.create_or_update_create_project_type_error_data)
    def test_create_or_update_create_project_type_error(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create project with
        incorrect parameter types"""
        expected = {self.ts.error: "project object: must be python dictionary"}

        for param in data_in[0]:
            ts_parameters = [param] + data_in[1:]

            result = self.ts._TimeSync__create_or_update(*ts_parameters)

            assert result == expected

    @pymesync_test(test_data.create_or_update_create_activity_valid_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_create_activity_valid(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        valid data"""
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_update_activity_valid_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_update_activity_valid(self, data_in, data_out, mock_post):
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        mock_post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_update_activity_valid_less_fields_data,
                   patch_names=["pymesync.pymesync.requests.post"])
    def test_create_or_update_update_activity_valid_less_fields(self, data_in, data_out, mock_post):
        """Tests TimeSync._TimeSync__create_or_update for update activity with
        one valid parameter"""
        # Send it
        self.ts._TimeSync__create_or_update(*data_in)

        # Test it
        self.mock_requests.post.assert_called_with(*data_out[0], **data_out[1])

    @pymesync_test(test_data.create_or_update_create_activity_invalid_data)
    def test_create_or_update_create_activity_invalid(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        invalid field"""
        expected = {self.ts.error: "activity object: invalid field: bad"}

        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_activity_required_missing_data)
    def test_create_or_update_create_activity_required_missing(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        missing required fields"""
        expected = {self.ts.error: "activity object: missing required "
                                   "field(s): slug"}

        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_activity_each_required_missing_data)
    def test_create_or_update_create_activity_each_required_missing(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        missing required fields"""
        # Parameters to be sent to TimeSync
        activity = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        activity = dict(data_in[0])

        for key in data_in[0]:
            del(activity[key])

            expected = {self.ts.error: "activity object: missing required "
                                       "field(s): {}".format(key)}

            ts_parameters = [activity] + data_in[1:]

            result = self.ts._TimeSync__create_or_update(*ts_parameters)

            assert result == expected

            activity = dict(data_in[0])

    @pymesync_test(test_data.create_or_update_create_activity_type_error_data)
    def test_create_or_update_create_activity_type_error(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        incorrect parameter types"""
        expected = {self.ts.error: "activity object: must be python dictionary"}

        for param in data_in[0]:
            ts_parameters = [param] + data_in[1:]

            result = self.ts._TimeSync__create_or_update(*ts_parameters)

            assert result == expected

    @pymesync_test(test_data.create_or_update_create_time_no_auth_data)
    def test_create_or_update_create_time_no_auth(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create time with no
        auth"""
        expected = {self.ts.error: "Not authenticated with TimeSync, call "
                                   "self.authenticate() first"}

        self.ts.token = None

        # Send it
        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_user_no_auth_data)
    def test_create_or_update_create_user_no_auth(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create user with no
           auth"""
        expected = {self.ts.error: "Not authenticated with TimeSync, call "
                                   "self.authenticate() first"}

        self.ts.token = None

        #Send it
        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_project_no_auth_data)
    def test_create_or_update_create_project_no_auth(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create project with no
        auth"""
        expected = {self.ts.error: "Not authenticated with TimeSync, call "
                                  "self.authenticate() first"}

        self.ts.token = None

        #Send it
        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_create_activity_no_auth_data)
    def test_create_or_update_create_activity_no_auth(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for create activity with
        no auth"""
        expected = {self.ts.error: "Not authenticated with TimeSync, call "
                                  "self.authenticate() first"}

        self.ts.token = None

        #Send it
        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_update_time_no_auth_data)
    def test_create_or_update_update_time_no_auth(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for update time with no
        auth"""
        expected = {self.ts.error: "Not authenticated with TimeSync, call "
                                   "self.authenticate() first"}

        self.ts.token = None

        # Send it
        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_update_user_no_auth_data)
    def test_create_or_update_update_user_no_auth(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for update user with no
           auth"""
        expected = {self.ts.error: "Not authenticated with TimeSync, call "
                                   "self.authenticate() first"}

        self.ts.token = None

        #Send it
        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_update_project_no_auth_data)
    def test_create_or_update_update_project_no_auth(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for update project with no
        auth"""
        expected = {self.ts.error: "Not authenticated with TimeSync, call "
                                  "self.authenticate() first"}

        self.ts.token = None

        #Send it
        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.create_or_update_update_activity_no_auth_data)
    def test_create_or_update_update_activity_no_auth(self, data_in, data_out):
        """Tests TimeSync._TimeSync__create_or_update for update activity with
        no auth"""
        expected = {self.ts.error: "Not authenticated with TimeSync, call "
                                  "self.authenticate() first"}

        self.ts.token = None

        #Send it
        result = self.ts._TimeSync__create_or_update(*data_in)

        assert result == expected

    @pymesync_test(test_data.auth_data)
    def test_auth(self, data_in, data_out):
        """Tests TimeSync._TimeSync__auth function"""
        result = self.ts._TimeSync__auth()

        assert result == data_out

    @pymesync_test(test_data.get_time_for_user_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_user(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with username query parameter"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_for_proj_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_proj(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with project query parameter"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_for_activity_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_activity(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with activity query parameter"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_for_start_date_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_start_date(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with start date query parameter"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_for_end_date_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_end_date(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with end date query parameter"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_for_include_revisions_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_include_revisions(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with include_revisions query parameter"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_for_include_revisions_false_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_include_revisions_false(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with include_revisions False query
        parameter"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_for_include_deleted_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_include_deleted(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with include_deleted query parameter"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_for_include_deleted_false_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_include_deleted_false(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with include_revisions False query
        parameter"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_for_proj_and_activity_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_proj_and_activity(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with project and activity query
        parameters"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameters
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_for_activity_x3_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_for_activity_x3(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with project and activity query
        parameters"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameters
        # Multiple parameters are sorted alphabetically
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_with_uuid_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_with_uuid(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with uuid query parameter"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_with_uuid_and_activity_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_with_uuid_and_activity(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with uuid and activity query parameters"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        # Test that requests.get was called with baseurl and correct parameter
        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    @pymesync_test(test_data.get_time_with_uuid_and_include_revisions_data,
                   patch_names=["pymesync.pymesync.requests.get"])
    def test_get_time_with_uuid_and_include_revisions(self, data_in, data_out, mock_get):
        """Tests TimeSync.get_times with uuid and include_revisions query
        parameters"""
        response = resp()
        response.text = json.dumps(data_out[0])

        mock_get.return_value = response

        result = self.ts.get_times(data_in)

        assert result == [data_out[0]]
        mock_get.assert_called_with(data_out[1])

    def test_get_time_with_uuid_and_include_deleted(self):
        """Tests TimeSync.get_times with uuid and include_deleted query
        parameters"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        url = "{0}/times/sadfasdg432?include_deleted=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Test that requests.get was called with baseurl and correct parameter
        self.assertEquals(self.ts.get_times({"uuid": "sadfasdg432",
                                             "include_deleted": True}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_time_with_uuid_include_deleted_and_revisions(self):
        """Tests TimeSync.get_times with uuid and include_deleted query
        parameters"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        # Please forgive me for this. I blame the PEP8 line length rule
        endpoint = "times"
        uuid = "sadfasdg432"
        token = "token={}".format(self.ts.token)
        queries = "include_deleted=true&include_revisions=true"
        url = "{0}/{1}/{2}?{3}&{4}".format(self.ts.baseurl, endpoint, uuid,
                                           queries, token)

        # Test that requests.get was called with baseurl and correct parameter
        self.assertEquals(self.ts.get_times({"uuid": "sadfasdg432",
                                             "include_revisions": True,
                                             "include_deleted": True}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_all_times(self):
        """Tests TimeSync.get_times with no parameters"""
        response = resp()
        response.text = json.dumps([{"this": "should be in a list"}])

        self.mock_requests.get.return_value = response

        url = "{0}/times?token={1}".format(self.ts.baseurl,
                                           self.ts.token)

        # Test that requests.get was called with baseurl and correct parameter
        self.assertEquals(self.ts.get_times(),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_times_bad_query(self):
        """Tests TimeSync.get_times with an invalid query parameter"""
        # Should return the error
        self.assertEquals(self.ts.get_times({"bad": ["query"]}),
                          [{self.ts.error: "invalid query: bad"}])

    def test_get_projects(self):
        """Tests TimeSync.get_projects"""
        response = resp()
        response.text = json.dumps([{"this": "should be in a list"}])

        self.mock_requests.get.return_value = response

        url = "{0}/projects?token={1}".format(self.ts.baseurl,
                                              self.ts.token)

        # Test that requests.get was called correctly
        self.assertEquals(self.ts.get_projects(),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_projects_slug(self):
        """Tests TimeSync.get_projects with slug"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        url = "{0}/projects/gwm?token={1}".format(self.ts.baseurl,
                                                  self.ts.token)

        # Test that requests.get was called correctly
        self.assertEquals(self.ts.get_projects({"slug": "gwm"}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_projects_include_revisions(self):
        """Tests TimeSync.get_projects with include_revisions query"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        url = "{0}/projects?include_revisions=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Test that requests.get was called correctly
        self.assertEquals(self.ts.get_projects({"include_revisions": True}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_projects_slug_include_revisions(self):
        """Tests TimeSync.get_projects with include_revisions query and slug"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        url = "{0}/projects/gwm?include_revisions=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it

        # Test that requests.get was called correctly
        self.assertEquals(self.ts.get_projects({"slug": "gwm",
                                                "include_revisions": True}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_projects_include_deleted(self):
        """Tests TimeSync.get_projects with include_deleted query"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        url = "{0}/projects?include_deleted=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Test that requests.get was called correctly
        self.assertEquals(self.ts.get_projects({"include_deleted": True}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_projects_include_deleted_with_slug(self):
        """Tests TimeSync.get_projects with include_deleted query and slug,
        which is not allowed"""

        # Test that error message is returned, can't combine slug and
        # include_deleted
        self.assertEquals(self.ts.get_projects({"slug": "gwm",
                                                "include_deleted": True}),
                          [{self.ts.error:
                           "invalid combination: slug and include_deleted"}])

    def test_get_projects_include_deleted_include_revisions(self):
        """Tests TimeSync.get_projects with include_revisions and
        include_deleted queries"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        token_string = "&token={}".format(self.ts.token)
        endpoint = "/projects"
        url = "{0}{1}?include_deleted=true&include_revisions=true{2}".format(
            self.ts.baseurl, endpoint, token_string)

        # Test that requests.get was called with correct parameters
        self.assertEquals(self.ts.get_projects({"include_revisions": True,
                                                "include_deleted": True}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_activities(self):
        """Tests TimeSync.get_activities"""
        response = resp()
        response.text = json.dumps([{"this": "should be in a list"}])

        self.mock_requests.get.return_value = response

        url = "{0}/activities?token={1}".format(self.ts.baseurl, self.ts.token)

        # Test that requests.get was called correctly
        self.assertEquals(self.ts.get_activities(),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_activities_slug(self):
        """Tests TimeSync.get_activities with slug"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        url = "{0}/activities/code?token={1}".format(self.ts.baseurl,
                                                     self.ts.token)

        # Test that requests.get was called correctly
        self.assertEquals(self.ts.get_activities({"slug": "code"}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_activities_include_revisions(self):
        """Tests TimeSync.get_activities with include_revisions query"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        url = "{0}/activities?include_revisions=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Test that requests.get was called correctly
        self.assertEquals(self.ts.get_activities({"include_revisions": True}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_activities_slug_include_revisions(self):
        """Tests TimeSync.get_projects with include_revisions query and slug"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        url = "{0}/activities/code?include_revisions=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Test that requests.get was called correctly
        self.assertEquals(self.ts.get_activities({"slug": "code",
                                                  "include_revisions": True}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_activities_include_deleted(self):
        """Tests TimeSync.get_activities with include_deleted query"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        url = "{0}/activities?include_deleted=true&token={1}".format(
            self.ts.baseurl, self.ts.token)

        # Send it

        # Test that requests.get was called correctly
        self.assertEquals(self.ts.get_activities({"include_deleted": True}),
                          [{"this": "should be in a list"}])
        self.mock_requests.get.assert_called_with(url)

    def test_get_activities_include_deleted_with_slug(self):
        """Tests TimeSync.get_activities with include_deleted query and slug,
        which is not allowed"""

        # Test that error message is returned, can't combine slug and
        # include_deleted
        self.assertEquals(self.ts.get_activities({"slug": "code",
                                                  "include_deleted": True}),
                          [{self.ts.error:
                           "invalid combination: slug and include_deleted"}])

    def test_get_activities_include_deleted_include_revisions(self):
        """Tests TimeSync.get_activities with include_revisions and
        include_deleted queries"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        self.mock_requests.get.return_value = response

        token_string = "&token={}".format(self.ts.token)
        endpoint = "/activities"
        url = "{0}{1}?include_deleted=true&include_revisions=true{2}".format(
            self.ts.baseurl, endpoint, token_string)

        # Send it
        self.assertEquals(self.ts.get_activities({"include_revisions": True,
                                                 "include_deleted": True}),
                          [{"this": "should be in a list"}])

        # Test that requests.get was called with correct parameters
        self.mock_requests.get.assert_called_with(url)

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

    def test_get_users(self):
        """Tests TimeSync.get_users"""
        response = resp()
        response.text = json.dumps([{"this": "should be in a list"}])

        url = "{0}/users?token={1}".format(self.ts.baseurl, self.ts.token)

        self.mock_requests.get.return_value = response

        # Send it
        self.assertEquals(self.ts.get_users(),
                          [{"this": "should be in a list"}])

        # Test that requests.get was called correctly
        self.mock_requests.get.assert_called_with(url)

    def test_get_users_username(self):
        """Tests TimeSync.get_users with username"""
        response = resp()
        response.text = json.dumps({"this": "should be in a list"})

        url = "{0}/users/{1}?token={2}".format(self.ts.baseurl,
                                               "example-user",
                                               self.ts.token)

        self.mock_requests.get.return_value = response

        # Send it
        self.assertEquals(self.ts.get_users("example-user"),
                          [{"this": "should be in a list"}])

        # Test that requests.get was called correctly
        self.mock_requests.get.assert_called_with(url)

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

        python_object = {
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
        """Check that __response_to_python returns correctly for delete_*G
        methods"""
        response = resp()
        response.text = ""
        response.status_code = 200
        self.assertEquals(self.ts._TimeSync__response_to_python(response),
                          {"status": 200})

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_create_time(self, mock_create_or_update):
        """Tests that TimeSync.create_time calls _create_or_update with correct
        parameters"""
        time = {
            "duration": 12,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.ts.create_time(time)

        mock_create_or_update.assert_called_with(time, None, "time", "times")

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_update_time(self, mock_create_or_update):
        """Tests that TimeSync.update_time calls _create_or_update with correct
        parameters"""
        time = {
            "duration": 12,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.ts.update_time(time, "uuid")

        mock_create_or_update.assert_called_with(time, "uuid", "time",
                                                 "times", False)

    def test_create_time_with_negative_duration(self):
        """Tests that TimeSync.create_time will return an error if a negative
        duration is passed"""
        time = {
            "duration": -12600,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts.create_time(time),
                          {self.ts.error:
                           "time object: duration cannot be negative"})

    def test_update_time_with_negative_duration(self):
        """Tests that TimeSync.update_time will return an error if a negative
        duration is passed"""
        time = {
            "duration": -12600,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts.update_time(time, "uuid"),
                          {self.ts.error:
                           "time object: duration cannot be negative"})

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_create_time_with_string_duration(self, mock_create_or_update):
        """Tests that TimeSync.create_time will convert a string duration to
        the correct number of seconds"""
        time = {
            "duration": "3h30m",
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.ts.create_time(time)

        expected = {
            "duration": 12600,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        mock_create_or_update.assert_called_with(expected, None, "time",
                                                 "times")

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_update_time_with_string_duration(self, mock_create_or_update):
        """Tests that TimeSync.update_time will convert a string duration to
        the correct number of seconds"""
        time = {
            "duration": "3h30m",
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.ts.update_time(time, "uuid")

        expected = {
            "duration": 12600,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        mock_create_or_update.assert_called_with(expected, "uuid", "time",
                                                 "times", False)

    def test_create_time_with_junk_string_duration(self):
        """Tests that TimeSync.create_time will fail if a string containing no
        hours/minutes is entered"""
        time = {
            "duration": "junktime",
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts.create_time(time),
                          [{self.ts.error:
                            "time object: invalid duration string"}])

    def test_update_time_with_junk_string_duration(self):
        """Tests that TimeSync.update_time will fail if a string containing no
        hours/minutes is entered"""
        time = {
            "duration": "junktime",
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts.update_time(time, "uuid"),
                          [{self.ts.error:
                            "time object: invalid duration string"}])

    def test_create_time_with_invalid_string_duration(self):
        """Tests that TimeSync.create_time will fail if a string containing
        multiple hours/minutes is entered"""
        time = {
            "duration": "3h30m15h",
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts.create_time(time),
                          [{self.ts.error:
                            "time object: invalid duration string"}])

    def test_update_time_with_invalid_string_duration(self):
        """Tests that TimeSync.update_time will fail if a string containing
        multiple hours/minutes is entered"""
        time = {
            "duration": "3h30m15h",
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts.update_time(time, "uuid"),
                          [{self.ts.error:
                            "time object: invalid duration string"}])

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_create_project(self, mock_create_or_update):
        """Tests that TimeSync.create_project calls _create_or_update with
        correct parameters"""
        project = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
        }

        self.ts.create_project(project)
        mock_create_or_update.assert_called_with(project, None,
                                                 "project", "projects")

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_update_project(self, mock_create_or_update):
        """Tests that TimeSync.update_time calls _create_or_update with correct
        parameters"""
        project = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
        }

        self.ts.update_project(project, "slug")
        mock_create_or_update.assert_called_with(project, "slug", "project",
                                                 "projects", False)

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_create_activity(self, mock_create_or_update):
        """Tests that TimeSync.create_activity calls _create_or_update with
        correct parameters"""
        activity = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        self.ts.create_activity(activity)
        mock_create_or_update.assert_called_with(activity, None,
                                                 "activity", "activities")

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_update_activity(self, mock_create_or_update):
        """Tests that TimeSync.update_activity calls _create_or_update with
        correct parameters"""
        activity = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
        }

        self.ts.update_activity(activity, "slug")
        mock_create_or_update.assert_called_with(activity, "slug", "activity",
                                                 "activities", False)

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_create_user(self, mock_create_or_update):
        """Tests that TimeSync.create_user calls _create_or_update with correct
        parameters"""
        user = {
            "username": "example-user",
            "password": "password",
            "display_name": "Example User",
            "email": "example.user@example.com",
        }

        self.ts.create_user(user)

        mock_create_or_update.assert_called_with(user, None, "user", "users")

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_create_user_valid_perms(self, mock_create_or_update):
        """Tests that TimeSync.create_user calls _create_or_update with correct
        parameters and valid permission fields"""
        user = {
            "username": "example-user",
            "password": "password",
            "display_name": "Example User",
            "email": "example.user@example.com",
            "site_admin": False,
            "site_spectator": False,
            "site_manager": True,
        }

        self.ts.create_user(user)

        mock_create_or_update.assert_called_with(user, None, "user", "users")
        self.assertEquals(bcrypt.hashpw("password", user["password"]),
                          user["password"])

    def test_create_user_invalid_admin(self):
        """Tests that TimeSync.create_user returns error with invalid perm
        field"""
        user = {
            "username": "example-user",
            "password": "password",
            "display_name": "Example User",
            "email": "example.user@example.com",
            "site_admin": True,
            "site_spectator": False,
            "site_manager": True,
            "active": True,
        }

        user_to_test = dict(user)
        for perm in ["site_admin", "site_spectator", "site_manager", "active"]:
            user_to_test = dict(user)
            user_to_test[perm] = "invalid"
            self.assertEquals(self.ts.create_user(user_to_test),
                              {self.ts.error: "user object: {} must be "
                                              "True or False".format(perm)})

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_create_user_unicode_password(self, mock_create_or_update):
        """Tests that unicode password objects get encoded to UTF-8 before
        being hashed"""
        user = {
            "username": "example-user",
            "password": u"password",
            "display_name": "Example User",
            "email": "example.user@example.com",
            "site_admin": True,
            "site_spectator": False,
            "site_manager": True,
            "active": True,
        }

        encoded_password = user["password"].encode("utf-8")

        self.ts.create_user(user)

        self.assertEquals(bcrypt.hashpw(encoded_password, user["password"]),
                          user["password"])

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_update_user(self, mock_create_or_update):
        """Tests that TimeSync.update_user calls _create_or_update with correct
        parameters"""
        user = {
            "username": "example-user",
            "password": "password",
            "display_name": "Example User",
            "email": "example.user@example.com",
        }

        self.ts.update_user(user, "example")
        mock_create_or_update.assert_called_with(user, "example", "user",
                                                 "users", False)
        self.assertEquals(bcrypt.hashpw("password", user["password"]),
                          user["password"])

    @patch("pymesync.TimeSync._TimeSync__create_or_update")
    def test_update_user_unicode_password(self, mock_create_or_update):
        """Tests that unicode password objects get encoded to UTF-8 before
        being hashed"""
        user = {
            "username": "example-user",
            "password": u"password",
            "display_name": "Example User",
            "email": "example.user@example.com",
            "site_admin": True,
            "site_spectator": False,
            "site_manager": True,
            "active": True,
        }

        encoded_password = user["password"].encode("utf-8")

        self.ts.update_user(user, user["username"])

        self.assertEquals(bcrypt.hashpw(encoded_password, user["password"]),
                          user["password"])

    def test_authentication(self):
        """Tests authenticate method for url and data construction"""
        auth = {
            "auth": {
                "type": "password",
                "username": "example-user",
                "password": "password"
            }
        }

        self.ts.authenticate("example-user", "password", "password")

        self.mock_requests.post.assert_called_with("http://ts.example.com/v1/login",
                                                   json=auth)

    def test_authentication_return_success(self):
        """Tests authenticate method with a token return"""
        # Use this fake response object for mocking requests.post
        response = resp()
        response.text = json.dumps({"token": "sometoken"})

        self.mock_requests.post.return_value = response

        auth_block = self.ts.authenticate("example-user",
                                          "password",
                                          "password")

        self.assertEquals(auth_block["token"], self.ts.token, "sometoken")
        self.assertEquals(auth_block, {"token": "sometoken"})

    def test_authentication_return_error(self):
        """Tests authenticate method with an error return"""
        # Use this fake response object for mocking requests.post
        response = resp()
        response.text = json.dumps({"status": 401,
                                    "error": "Authentication failure",
                                    "text": "Invalid username or password"})

        self.mock_requests.post.return_value = response

        auth_block = self.ts.authenticate("example-user",
                                          "password",
                                          "password")

        self.assertEquals(auth_block, {"status": 401,
                                       "error": "Authentication failure",
                                       "text": "Invalid username or "
                                       "password"})

    def test_authentication_no_username(self):
        """Tests authenticate method with no username in call"""
        self.assertEquals(self.ts.authenticate(password="password",
                                               auth_type="password"),
                          {self.ts.error: "Missing username; "
                           "please add to method call"})

    def test_authentication_no_password(self):
        """Tests authenticate method with no password in call"""
        self.assertEquals(self.ts.authenticate(username="username",
                                               auth_type="password"),
                          {self.ts.error: "Missing password; "
                           "please add to method call"})

    def test_authentication_no_auth_type(self):
        """Tests authenticate method with no auth_type in call"""
        self.assertEquals(self.ts.authenticate(password="password",
                                               username="username"),
                          {self.ts.error: "Missing auth_type; "
                           "please add to method call"})

    def test_authentication_no_username_or_password(self):
        """Tests authenticate method with no username or password in call"""
        self.assertEquals(self.ts.authenticate(auth_type="password"),
                          {self.ts.error: "Missing username, password; "
                           "please add to method call"})

    def test_authentication_no_username_or_auth_type(self):
        """Tests authenticate method with no username or auth_type in call"""
        self.assertEquals(self.ts.authenticate(password="password"),
                          {self.ts.error: "Missing username, auth_type; "
                           "please add to method call"})

    def test_authentication_no_password_or_auth_type(self):
        """Tests authenticate method with no username or auth_type in call"""
        self.assertEquals(self.ts.authenticate(username="username"),
                          {self.ts.error: "Missing password, auth_type; "
                           "please add to method call"})

    def test_authentication_no_arguments(self):
        """Tests authenticate method with no arguments in call"""
        self.assertEquals(self.ts.authenticate(),
                          {self.ts.error: "Missing username, password, "
                           "auth_type; please add to method call"})

    def test_authentication_no_token_in_response(self):
        """Tests authenticate method with no token in response"""
        response = resp()
        response.status_code = 502

        self.mock_requests.post.return_value = response

        self.assertEquals(self.ts.authenticate(username="username",
                                               password="password",
                                               auth_type="password"),
                          {self.ts.error:
                           "connection to TimeSync failed at baseurl "
                           "http://ts.example.com/v1 - "
                           "response status was 502"})

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
                          {self.ts.error:
                           "connection to TimeSync failed at baseurl "
                           "http://ts.example.com/v1 - "
                           "response status was 502"})

    def test_delete_object_time(self):
        """Test that _delete_object calls requests.delete with the correct
        url"""
        url = "{0}/times/abcd-3453-3de3-99sh?token={1}".format(self.ts.baseurl,
                                                               self.ts.token)
        self.ts._TimeSync__delete_object("times", "abcd-3453-3de3-99sh")
        self.mock_requests.delete.assert_called_with(url)

    def test_delete_object_project(self):
        """Test that _delete_object calls requests.delete with the correct
        url"""
        url = "{0}/projects/ts?token={1}".format(self.ts.baseurl,
                                                 self.ts.token)
        self.ts._TimeSync__delete_object("projects", "ts")
        self.mock_requests.delete.assert_called_with(url)

    def test_delete_object_activity(self):
        """Test that _delete_object calls requests.delete with the correct
        url"""
        url = "{0}/activities/code?token={1}".format(self.ts.baseurl,
                                                     self.ts.token)
        self.ts._TimeSync__delete_object("activities", "code")
        self.mock_requests.delete.assert_called_with(url)

    def test_delete_object_user(self):
        """Test that _delete_object calls requests.delete with the correct
        url"""
        url = "{0}/users/example-user?token={1}".format(self.ts.baseurl,
                                                        self.ts.token)
        self.ts._TimeSync__delete_object("users", "example-user")
        self.mock_requests.delete.assert_called_with(url)

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
                          {"pymesync error":
                           "Not authenticated with TimeSync, "
                           "call self.authenticate() first"})

    def test_delete_time_no_uuid(self):
        """Test that delete_time returns proper error when uuid not provided"""
        self.assertEquals(self.ts.delete_time(),
                          {"pymesync error":
                           "missing uuid; please add to method call"})

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
                          {"pymesync error":
                           "Not authenticated with TimeSync, "
                           "call self.authenticate() first"})

    def test_delete_project_no_slug(self):
        """Test that delete_project returns proper error when slug not
        provided"""
        self.assertEquals(self.ts.delete_project(),
                          {"pymesync error":
                           "missing slug; please add to method call"})

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
                          {"pymesync error":
                           "Not authenticated with TimeSync, "
                           "call self.authenticate() first"})

    def test_delete_activity_no_slug(self):
        """Test that delete_activity returns proper error when slug not
        provided"""
        self.assertEquals(self.ts.delete_activity(),
                          {"pymesync error":
                           "missing slug; please add to method call"})

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
                          {"pymesync error":
                           "Not authenticated with TimeSync, "
                           "call self.authenticate() first"})

    def test_delete_user_no_username(self):
        """Test that delete_user returns proper error when username not
        provided"""
        self.assertEquals(self.ts.delete_user(),
                          {"pymesync error":
                           "missing username; please add to method call"})

    def test_token_expiration_valid(self):
        """Test that token_expiration_time returns valid date from a valid
        token"""
        self.ts.token = ("eyJ0eXAiOiJKV1QiLCJhbGciOiJITUFDLVNIQTUxMiJ9.eyJpc3M"
                         "iOiJvc3Vvc2wtdGltZXN5bmMtc3RhZ2luZyIsInN1YiI6InRlc3Q"
                         "iLCJleHAiOjE0NTI3MTQzMzQwODcsImlhdCI6MTQ1MjcxMjUzNDA"
                         "4N30=.QP2FbiY3I6e2eN436hpdjoBFbW9NdrRUHbkJ+wr9GK9mMW"
                         "7/oC/oKnutCwwzMCwjzEx6hlxnGo6/LiGyPBcm3w==")

        decoded_payload = base64.b64decode(self.ts.token.split(".")[1])
        exp_int = ast.literal_eval(decoded_payload)['exp'] / 1000
        exp_datetime = datetime.datetime.fromtimestamp(exp_int)

        self.assertEquals(self.ts.token_expiration_time(),
                          exp_datetime)

    def test_token_expiration_invalid(self):
        """Test that token_expiration_time returns correct from an invalid
        token"""
        self.assertEquals(self.ts.token_expiration_time(),
                          {self.ts.error: "improperly encoded token"})

    def test_token_expiration_no_auth(self):
        """Test that token_expiration_time returns correct error when user is
        not authenticated"""
        self.ts.token = None
        self.assertEquals(self.ts.token_expiration_time(),
                          {self.ts.error: "Not authenticated with TimeSync, "
                                          "call self.authenticate() first"})

    def test_duration_to_seconds(self):
        """Tests that when a string duration is entered, it is converted to an
        integer"""
        time = {
            "duration": "3h30m",
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts._TimeSync__duration_to_seconds
                          (time['duration']), 12600)

    def test_duration_to_seconds_with_invalid_str(self):
        """Tests that when an invalid string duration is entered, an error
        message is returned"""
        time = {
            "duration": "3hh30m",
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts._TimeSync__duration_to_seconds
                          (time['duration']),
                          [{self.ts.error:
                            "time object: invalid duration string"}])

    def test_hash_user_password_unicode(self):
        """Tests that unicode passwords are hashed correctly"""
        user = {
            u"username": u"user",
            u"password": u"pass"
        }

        encoded_password = user["password"].encode("utf-8")

        self.ts._TimeSync__hash_user_password(user)

        self.assertEquals(bcrypt.hashpw(encoded_password, user["password"]),
                          user["password"])

    def test_hash_user_password_nonunicode(self):
        """Tests that non-unicode passwords are hashed correctly"""
        user = {
            "username": "user",
            "password": "pass"
        }

        password = user["password"]

        self.ts._TimeSync__hash_user_password(user)

        self.assertEquals(bcrypt.hashpw(password, user["password"]),
                          user["password"])

    def test_duration_invalid(self):
        """Tests for duration validity - if the duration given is a negative
        int, an error message is returned"""
        time = {
            "duration": -12600,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17",
        }

        self.assertEquals(self.ts.create_time(time),
                          {self.ts.error:
                           "time object: duration cannot be negative"})

    def test_project_users_valid(self):
        """Test project_users method with a valid project object returned from
        TimeSync"""
        project = "pyme"
        response = resp()
        response.status_code = 200
        response.text = json.dumps({
            "uri": "https://github.com/osuosl/pymesync",
            "name": "pymesync",
            "slugs": ["pyme", "ps", "pymesync"],
            "uuid": "a034806c-00db-4fe1-8de8-514575f31bfb",
            "revision": 4,
            "created_at": "2014-07-17",
            "deleted_at": None,
            "updated_at": "2014-07-20",
            "users": {
                "malcolm": {"member": True,
                            "manager": True,
                            "spectator": True},
                "jayne":   {"member": True,
                            "manager": False,
                            "spectator": False},
                "kaylee":  {"member": True,
                            "manager": False,
                            "spectator": False},
                "zoe":     {"member": True,
                            "manager": False,
                            "spectator": False},
                "hoban":   {"member": True,
                            "manager": False,
                            "spectator": False},
                "simon":   {"member": False,
                            "manager": False,
                            "spectator": True},
                "river":   {"member": False,
                            "manager": False,
                            "spectator": True},
                "derrial": {"member": False,
                            "manager": False,
                            "spectator": True},
                "inara":   {"member": False,
                            "manager": False,
                            "spectator": True}
            }
        })

        self.mock_requests.get.return_value = response

        expected_result = {
            u'malcolm': [u'member', u'manager', u'spectator'],
            u'jayne':   [u'member'],
            u'kaylee':  [u'member'],
            u'zoe':     [u'member'],
            u'hoban':   [u'member'],
            u'simon':   [u'spectator'],
            u'river':   [u'spectator'],
            u'derrial': [u'spectator'],
            u'inara':   [u'spectator']
        }

        self.assertEquals(self.ts.project_users(project=project),
                          expected_result)

    def test_project_users_error_response(self):
        """Test project_users method with an error object returned from
        TimeSync"""
        proj = "pymes"
        response = resp()
        response.status_code = 404
        response.text = json.dumps({
            "error": "Object not found",
            "text": "Nonexistent project"
        })

        self.mock_requests.get.return_value = response

        self.assertEquals(self.ts.project_users(project=proj),
                          {u"error": u"Object not found",
                           u"text": u"Nonexistent project"})

    def test_project_users_no_project_parameter(self):
        """Test project_users method with no project object passed as a
        parameter, should return an error"""
        self.assertEquals(self.ts.project_users(),
                          {self.ts.error: "Missing project slug, please "
                                          "include in method call"})

    def test_baseurl_with_trailing_slash(self):
        """Test that the trailing slash in the baseurl is removed"""
        self.ts = pymesync.TimeSync("http://ts.example.com/v1/")
        self.assertEquals(self.ts.baseurl, "http://ts.example.com/v1")

    def test_baseurl_without_trailing_slash(self):
        """Test that the trailing slash in the baseurl is removed"""
        self.ts = pymesync.TimeSync("http://ts.example.com/v1")
        self.assertEquals(self.ts.baseurl, "http://ts.example.com/v1")
