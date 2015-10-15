"""
pymesync - Python TimeSync Module

Allows for interactions with the TimeSync API
- timesync.send_time(baseurl) -- Sends time to baseurl (TimeSync)
"""
import errno
import json
import requests


class TimeSync(object):

    def __init__(self, baseurl, user, password, auth_type):
        self.baseurl = baseurl
        self.user = user
        self.password = password
        self.auth_type = auth_type

    def send_time(self, post_request):
        """
        send_time(post_request)

        Sends a POST request in a JSON body to TimeSync, returns that body if
        successful or an error
        """

        values = {
            'auth': self._auth(),
            'object': {
                'duration': post_request['duration'],
                'user': post_request['user'],
                'project': post_request['project'],
                'activities': post_request['activities'],
                'date_worked': post_request['date_worked'],
                'notes': post_request['notes'],
                'issue_uri': post_request['issue_uri'],
            }
        }

        # Convert post_request to JSON object
        json_content = json.dumps(values)

        # Construct url to post to
        url = "{}/v1/times".format(self.baseurl)

        # Attempt to POST to TimeSync
        try:
            # Success!
            response = requests.post(url, json=json_content)
            return response
        except requests.exceptions.RequestException as e:
            # Unknown request error
            return e

    def _auth(self):
        """Returns auth object to be send to TimeSync"""
        return {'type': self.auth_type,
                'username': self.user,
                'password': self.password, }
