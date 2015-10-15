import unittest
import timesync
import urllib2
import httplib
import mock
import requests
import json
import errno

class TestTimeSync(unittest.TestCase):

    def test_send_time_valid(self):
        """Tests TimeSync.send_time with valid data"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
            "project": "ganet_web_manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes":"Worked on docs",
            "issue_uri":"https://github.com/",
            "date_worked":2014-04-17,
        }

        # Test baseurl
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = timesync.TimeSync(baseurl,
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
        json_content = str.encode(json_content)

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.Mock()

        # Send it
        ts.send_time(params)

        # Test it
        requests.post.assert_called_with('http://ts.example.com/v1/times',
                                         data=json_content)

    def test_send_time_catch_HTTPError(self):
        """Tests TimeSync.send_time with HTTPError"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
            "project": "ganet_web_manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes":"Worked on docs",
            "issue_uri":"https://github.com/",
            "date_worked":2014-04-17,
        }

        # Test baseurl
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = timesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.Mock(return_value=requests.exceptions.HTTPError)

        self.assertEquals(ts.send_time(params), errno.ENETDOWN)

    def test_send_time_catch_ConnectionError(self):
        """Tests TimeSync.send_time with HTTPError"""
        # Parameters to be sent to TimeSync
        params = {
            "duration": 12,
            "project": "ganet_web_manager",
            "user": "example-user",
            "activities": ["documenting"],
            "notes":"Worked on docs",
            "issue_uri":"https://github.com/",
            "date_worked":2014-04-17,
        }

        # Test baseurl
        baseurl = 'http://ts.example.com'
        # Instantiate timesync class
        ts = timesync.TimeSync(baseurl,
                               password="password",
                               user="example-user",
                               auth_type="password")

        # Mock requests.post so it doesn't actually post to TimeSync
        requests.post = mock.Mock(
            return_value=requests.exceptions.ConnectionError)

        self.assertEquals(ts.send_time(params), errno.ENETUNREACH)



if __name__ == '__main__':
    unittest.main()
