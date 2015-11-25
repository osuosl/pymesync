"""
pymesync - Python TimeSync Module

Allows for interactions with the TimeSync API

- send_time(parameter_dict) - Sends time to baseurl (TimeSync)
- get_times([kwargs]) - Get times from TimeSync
- get_projects([kwargs]) - Get project information from TimeSync

Supported TimeSync versions:
v1
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
        self.error = "pymesync error"
        self.valid_get_queries = ["user", "project", "activity",
                                  "start", "end", "revisions"]

    def send_time(self, parameter_dict):
        """
        send_time(parameter_dict)

        Send a time entry to TimeSync via a POST request in a JSON body. This
        method will return that body in the form of a list containing a single
        python dictionary. The dictionary will contain a representation of that
        JSON body if it was successful or error information if it was not.

        ``parameter_dict`` is a python dictionary containing the time
        information to send to TimeSync.
        """
        values = {
            'auth': self._auth(),
            'object': parameter_dict,
        }

        # Construct url to post to
        url = "{}/times".format(self.baseurl)

        # Attempt to POST to TimeSync
        try:
            # Success!
            response = requests.post(url, json=values)
            return self._json_to_python(response.text)
        except requests.exceptions.RequestException as e:
            # Request error
            return e

    def get_times(self, **kwargs):
        """
        get_times([kwargs])

        Request time entries filtered by parameters passed to ``kwargs``.
        Returns a list of python objects representing the JSON time information
        returned by TimeSync or an error message if unsuccessful.

        ``kwargs`` contains the optional query parameters described in the
        TimeSync documentation. If ``kwargs`` is empty, ``get_times()`` will
        return all times in the database. The syntax for each argument is
        ``query=["parameter"]``.
        """
        query_list = []  # Remains empty if no kwargs passed
        query_string = ""
        if kwargs:
            if "id" in kwargs.keys():
                query_string = "/{}".format(kwargs['id'])
            else:
                # Sort them into an alphabetized list for easier testing
                sorted_qs = sorted(kwargs.items(), key=operator.itemgetter(0))
                for query, param in sorted_qs:
                    if query in self.valid_get_queries:
                        for slug in param:
                            query_list.append("{0}={1}".format(query, slug))
                    else:
                        return {self.error: "invalid query: {}".format(query)}

                query_string = "?{}".format(query_list[0])
                for string in query_list[1:]:
                    query_string += "&{}".format(string)

        # Construct query url
        url = "{0}/times{1}".format(self.baseurl,
                                    query_string)

        # Attempt to GET times
        try:
            # Success!
            response = requests.get(url)
            return self._json_to_python(response.text)
        except requests.exceptions.RequestException as e:
            # Request Error
            return e

    def get_projects(self, **kwargs):
        """
        get_times([kwargs])

        Request project information filtered by parameters passed to
        ``kwargs``. Returns a list of python objects representing the JSON
        project information returned by TimeSync or an error message if
        unsuccessful.

        ``kwargs`` contains the optional query parameters described in the
        TimeSync documentation. If ``kwargs`` is empty, ``get_projects()`` will
        return all projects in the database. The syntax for each argument is
        ``query="parameter"`` or ``bool_query=<boolean>``.

        Optional parameters:
        slug='<slug>'
        include_deleted=<boolean>
        revisions=<boolean>

        Does not accept a slug combined with include_deleted, but does accept
        any other combination.
        """
        query_string = ""
        query_list = []
        if kwargs:
            # The following combination is not allowed
            if 'slug' in kwargs.keys() and 'include_deleted' in kwargs.keys():
                error_message = "invalid combination: slug and include_deleted"
                return {self.error: error_message}
            # slug goes first, then delete it so it doesn't show up after the ?
            elif 'slug' in kwargs.keys():
                query_string = "/{}".format(kwargs['slug'])
                del(kwargs['slug'])

            # Convert True and False booleans to TimeSync compatible strings
            for k, v in sorted(kwargs.items(), key=operator.itemgetter(0)):
                kwargs[k] = 'true' if v else 'false'
                query_list.append("{0}={1}".format(k, kwargs[k]))

            # Check for items in query_list after slug was removed, create
            # query string
            if query_list:
                query_string += "?{}".format("&".join(query_list))

        # Construct query url - query_string is empty if no kwargs
        url = "{0}/projects{1}".format(self.baseurl,
                                       query_string)

        # Attempt to GET projects
        try:
            # Success!
            response = requests.get(url)
            return self._json_to_python(response.text)
        except requests.exceptions.RequestException as e:
            # Request Error
            return e

    def _auth(self):
        """Returns auth object to be send to TimeSync"""
        return {'type': self.auth_type,
                'username': self.user,
                'password': self.password, }

    def _json_to_python(self, json_object):
        """Convert json object to native python list of objects"""
        python_object = json.loads(str(json_object))

        if not isinstance(python_object, list):
            python_object = [python_object]

        return python_object
