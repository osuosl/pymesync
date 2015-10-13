"""
Python TimeSync Module

Allows for interactions with the TimeSync API
- timesync.report_time(baseurl) -- Reports time to baseurl
"""
import errno
import json
import urllib.error
import urllib.parse
import urllib.request


class TimeSync(object):

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def report_time(self, post_request):
        """
        report_time(post_request)

        Sends a POST request in a JSON body to TimeSync, returns that body or an
        error
        """
        # Convert post_request to JSON object
        data = json.dumps(post_request)
        data = str.encode(data)

        # Construct url to post to
        url = "{}/v1/times".format(self.baseurl)

        # Create the request
        req = urllib.request.Request(url, data,
                                     {'Content-Type': 'application/json'})
        # Attempt to POST to TimeSync
        try:
            # Success!
            with urllib.request.urlopen(req) as response:
                return response
        except urllib.error.HTTPError as e:
            # TimeSync error
            return e.read()
        except urllib.error.URLError as e:
            # Cannot reach server
            return e.read()
