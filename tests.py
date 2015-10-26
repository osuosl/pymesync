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

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.get = mock.create_autospec(requests.get)

        # Send it
        ts.get_times(user=ts.user)

        # Test that requests.get was called with baseurl and correct parameter
        requests.get.assert_called_with(
            'http://ts.example.com/v1/times/?user=:example_user')


if __name__ == '__main__':
    unittest.main()
