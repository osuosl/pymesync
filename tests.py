import unittest
import pymesync
import mock
import requests
import json


class TestPymesync(unittest.TestCase):

    def test_send_time_valid(self):
        """Tests TimeSync.send_time with valid data"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": 2014-04-17,
        }

        # Test baseurl
        baseurl = 'http://ts.example.com'
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
        # Convert to json for test
        json_content = json.dumps(content)

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.create_autospec(requests.post)

        # Send it
        ts.send_time(params)

        # Test it
        requests.post.assert_called_with('http://ts.example.com/v1/times',
                                         json=json_content)

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
            "date_worked": 2014-04-17,
        }

        # Test baseurl
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        self.assertRaises(Exception, ts.send_time(params))

    def test_auth(self):
        """Tests TimeSync._auth function"""
        # Test baseurl
        baseurl = 'http://ts.example.com'
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
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(user=ts.user)

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?user=example-user')

    def test_get_time_for_proj(self):
        """Tests TimeSync.get_times with project query parameter"""
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(project="gwm")

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?project=gwm')

    def test_get_time_for_activity(self):
        """Tests TimeSync.get_times with activity query parameter"""
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(activity="dev")

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?activity=dev')

    def test_get_time_for_start_date(self):
        """Tests TimeSync.get_times with start date query parameter"""
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(start="2015-07-23")

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?start=2015-07-23')

    def test_get_time_for_end_date(self):
        """Tests TimeSync.get_times with end date query parameter"""
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(end="2015-07-23")

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?end=2015-07-23')

    def test_get_time_for_revisions(self):
        """Tests TimeSync.get_times with revisions query parameter"""
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(revisions="true")

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?revisions=true')

    def test_get_time_for_proj_and_activity(self):
        """Tests TimeSync.get_times with project and activity query
        parameters"""
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times(project="gwm", activity="dev")

        # Test that requests.get was called with baseurl and correct parameters
        # Multiple paramaters are sorted alphabetically
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times?activity=dev?project=gwm')

    def test_get_all_times(self):
        """Tests TimeSync.get_times with no paramaters"""
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.get
        requests.get = mock.Mock('requests.get')

        # Send it
        ts.get_times()

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with('http://ts.example.com/v1/times')

    def test_get_times_bad_param(self):
        """Tests TimeSync.get_times with an invalid query parameter"""
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = pymesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Should return the error
        self.assertEquals("Error, invalid query: bad",
                          ts.get_times(bad="query"))


if __name__ == '__main__':
    unittest.main()
