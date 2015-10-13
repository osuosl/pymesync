"""
Webapp for TimeSync
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
        data = json.dumps(post_request)
        data = str.encode(data)

        url = "{}/v1/times".format(self.baseurl)

        req = urllib.request.Request(url, data,
                                     {'Content-Type': 'application/json'})
        try:
            # Success!
            with urllib.request.urlopen(req) as response:
                return "success"
        except urllib.error.HTTPError as e:
            # TimeSync error
            return e.read()
        except urllib.error.URLError as e:
            # Cannot reach server
            return errno.ENETUNREACH
