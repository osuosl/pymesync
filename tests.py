import unittest
import timesync
import urllib2
import httplib

class TestTimeSync(unittest.TestCase):

    def test_post_time_valid(self):
        """
        Tests TimeSync.send_time(baseurl)
        """
        params =
        {
            "duration":12,
            "user": "example-2",
            "project": "ganet_web_manager",
            "activities": ["documenting"],
            "notes":"Worked on documentation toward settings configuration.",
            "issue_uri":"https://github.com/osu-cass/whats-fresh-api/issues/56",
            "date_worked":2014-04-17,
        }

        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}

        baseurl = 'http://osuosl.org'
        ts = timesync.TimeSync(baseurl)

        ts.send_time({'foo': 'bar'})

        urllib2.urlopen.assert_called_once()

if __name__ == '__main__':
    unittest.main()
