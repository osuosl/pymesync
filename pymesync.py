"""
pymesync - Python TimeSync Module

Allows for interactions with the TimeSync API
- timesync.send_time(baseurl) -- Sends time to baseurl (TimeSync)
"""
import json
import requests
import operator


class TimeSync(object):

    def __init__(self, baseurl, user, password, auth_type):
        self.baseurl = baseurl
        self.user = user
        self.password = password
        self.auth_type = auth_type
        self.valid_get_queries = ["user", "project", "activity",
                                  "start", "end", "revisions"]

    def send_time(self, parameter_dict):
        """
        send_time(parameter_dict)

        Sends a POST request in a JSON body to TimeSync, returns that body if
        successful or an error if not.
        parameter_dict - python dict containing time info.
        """
        values = {
            'auth': self._auth(),
            'object': parameter_dict,
        }

        # Convert parameter_dict to JSON object
        json_content = json.dumps(values)

        # Construct url to post to
        url = "{0}/{1}/times".format(self.baseurl, self._api_version())

        # Attempt to POST to TimeSync
        try:
            # Success!
            response = requests.post(url, json=json_content)
            return response
        except requests.exceptions.RequestException as e:
            # Request error
            return e

    def get_times(self, **kwargs):
        """
        get_times([kwargs])

        Returns JSON times objects filtered by supplied parameters
        """
        query_list = []  # Remains empty if no kwargs passed
        query_string = ""
        if kwargs:
            # Sort them into an alphabetized list for easier testing
            sorted_qs = sorted(kwargs.items(), key=operator.itemgetter(0))
            for query, param in sorted_qs:
                if query in self.valid_get_queries:
                    for slug in param:
                        query_list.append("{0}={1}".format(query, slug))
                else:
                    return "Error, invalid query: {}".format(query)

            query_string = "?{}".format(query_list[0])
            for string in query_list[1:]:
                query_string += "&{}".format(string)

        # Construct query url
        url = "{0}/{1}/times{2}".format(self.baseurl,
                                        self._api_version(),
                                        query_string)

        # Attempt to GET times
        try:
            # Success!
            response = requests.get(url)
            return response
        except requests.exceptions.RequestException as e:
            # Request Error
            return e

    def get_projects(self, **kwargs):
        """
        get_times([kwargs])

        Returns JSON times objects filtered by supplied parameters
        """
        query_string = ""
        if kwargs:
            # The following combination is not allowed
            if 'slug' in kwargs.keys() and 'include_deleted' in kwargs.keys():
                return "Error: invalid combination of slug and include_deleted"
            # slug goes first
            elif 'slug' in kwargs.keys():
                query_string = "/{}".format(kwargs['slug'])

            # Put include_deleted first for easier testing
            if 'include_deleted' in kwargs.keys():
                query_string += "?{0}={1}".format('include_deleted',
                                                  kwargs['include_deleted'])
                # If we got include_deleted, this needs to have an &
                if 'revisions' in kwargs.keys():
                    query_string += "&{0}={1}".format('revisions',
                                                      kwargs['revisions'])
            # If not, it needs a ?
            elif 'revisions' in kwargs.keys():
                query_string += "?{0}={1}".format('revisions',
                                                  kwargs['revisions'])

        # Construct query url - query_string is empty if no kwargs
        url = "{0}/{1}/projects{2}".format(self.baseurl,
                                           self._api_version(),
                                           query_string)

        # Attempt to GET projects
        try:
            # Success!
            response = requests.get(url)
            return response
        except requests.exceptions.RequestException as e:
            # Request Error
            return e

    def _auth(self):
        """Returns auth object to be send to TimeSync"""
        return {'type': self.auth_type,
                'username': self.user,
                'password': self.password, }

    def _api_version(self):
        """
        Queries API to find and return API version

        Currently this is hardcoded to API v1 since no others exist. When v2 is
        released, this will be updated to query the API and discover which
        version is being used.
        """
        return 'v1'
