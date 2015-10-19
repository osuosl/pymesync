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

    def send_time(self, parameter_dict):
        """
        send_time(parameter_dict)

        Sends a POST request in a JSON body to TimeSync, returns that body if
        successful or an error if not.
        parameter_dict - python dict containing time info.
        """

        values = {
            'auth': self._auth(),
            'object': {
                'duration': parameter_dict['duration'],
                'user': parameter_dict['user'],
                'project': parameter_dict['project'],
                'activities': parameter_dict['activities'],
                'date_worked': parameter_dict['date_worked'],
                'notes': parameter_dict['notes'],
                'issue_uri': parameter_dict['issue_uri'],
            }
        }

        # Convert parameter_dict to JSON object
        json_content = json.dumps(values)

        # Construct url to post to
        url = "{0}/{1}/times".format(self.baseurl, self.api_version())

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

    def api_version(self):
        """
        Queries API to find and return API version

        Currently this is hardcoded to API v1 since no others exist. When v2 is
        released, this will be updated to query the API and discover which
        version is being used.
        """

        return 'v1'
