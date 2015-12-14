"""
pymesync - Python TimeSync Module

Allows for interactions with the TimeSync API

- create_time(parameter_dict) - Sends time to baseurl (TimeSync)
- create_project(parameter_dict, slug="") - Creates or updates project
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
        self.required_params = {
            "time": ["duration", "project", "user",
                     "activities", "date_worked"],
            "project": ["uri", "name", "slugs", "owner"],
            "activity": ["name", "slug"],
        }
        self.optional_params = {
            "time": ["notes", "issue_uri"],
            "project": [],
            "activity": [],
        }

    def create_time(self, parameter_dict):
        """
        create_time(parameter_dict)

        Send a time entry to TimeSync via a POST request in a JSON body. This
        method will return that body in the form of a list containing a single
        python dictionary. The dictionary will contain a representation of that
        JSON body if it was successful or error information if it was not.

        ``parameter_dict`` is a python dictionary containing the time
        information to send to TimeSync.
        """
        return self._create_or_update(parameter_dict, None,
                                      "time", "times")

    def update_time(self, parameter_dict, uuid):
        """
        update_time(parameter_dict, uuid)

        Send a time entry update to TimeSync via a POST request in a JSON body.
        This method will return that body in the form of a list containing a
        single python dictionary. The dictionary will contain a representation
        of that updated time object if it was successful or error information
        if it was not.

        ``parameter_dict`` is a python dictionary containing the time
        information to send to TimeSync.
        ``uuid`` contains the uuid for a time entry to update.
        """
        return self._create_or_update(parameter_dict, uuid,
                                      "time", "times", False)

    def create_project(self, parameter_dict):
        """
        create_project(parameter_dict)

        Post a project to TimeSync via a POST request in a JSON body. This
        method will return that body in the form of a list containing a single
        python dictionary. The dictionary will contain a representation of that
        JSON body if it was successful or error information if it was not.

        ``parameter_dict`` is a python dictionary containing the project
        information to send to TimeSync.
        """
        return self._create_or_update(parameter_dict, None,
                                      "project", "projects")

    def update_project(self, parameter_dict, slug):
        """
        update_project(parameter_dict, slug)

        Send a project update to TimeSync via a POST request in a JSON body.
        This method will return that body in the form of a list containing a
        single python dictionary. The dictionary will contain a representation
        of that updated project object if it was successful or error
        information if it was not.

        ``parameter_dict`` is a python dictionary containing the project
        information to send to TimeSync.
        ``slug`` contains the slug for a project entry to update.
        """
        return self._create_or_update(parameter_dict, slug,
                                      "project", "projects", False)

    def create_activity(self, parameter_dict):
        """
        create_activity(parameter_dict, slug=None)

        Post an activity to TimeSync via a POST request in a JSON body. This
        method will return that body in the form of a list containing a single
        python dictionary. The dictionary will contain a representation of that
        JSON body if it was successful or error information if it was not.

        ``parameter_dict`` is a python dictionary containing the activity
        information to send to TimeSync.
        """
        return self._create_or_update(parameter_dict, None,
                                      "activity", "activities")

    def update_activity(self, parameter_dict, slug):
        """
        update_activity(parameter_dict, slug)

        Send an activity update to TimeSync via a POST request in a JSON body.
        This method will return that body in the form of a list containing a
        single python dictionary. The dictionary will contain a representation
        of that updated activity object if it was successful or error
        information if it was not.

        ``parameter_dict`` is a python dictionary containing the project
        information to send to TimeSync.
        ``slug`` contains the slug for an activity entry to update.
        """
        return self._create_or_update(parameter_dict, slug,
                                      "activity", "activities", False)

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
            if "uuid" in kwargs.keys():
                query_string = "/{}".format(kwargs["uuid"])
            else:
                # Sort them into an alphabetized list for easier testing
                sorted_qs = sorted(kwargs.items(), key=operator.itemgetter(0))
                for query, param in sorted_qs:
                    if query in self.valid_get_queries:
                        for slug in param:
                            query_list.append("{0}={1}".format(query, slug))
                    else:
                        return [
                            {self.error: "invalid query: {}".format(query)}
                        ]

                query_string = "?{}".format(query_list[0])
                for string in query_list[1:]:
                    query_string += "&{}".format(string)

        # Construct query url
        url = "{0}/times{1}".format(self.baseurl, query_string)

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
        get_projects([kwargs])

        Request project information filtered by parameters passed to
        ``kwargs``. Returns a list of python objects representing the JSON
        project information returned by TimeSync or an error message if
        unsuccessful.

        ``kwargs`` contains the optional query parameters described in the
        TimeSync documentation. If ``kwargs`` is empty, ``get_projects()`` will
        return all projects in the database. The syntax for each argument is
        ``query="parameter"`` or ``bool_query=<boolean>``.

        Optional parameters:
        slug="<slug>"
        include_deleted=<boolean>
        revisions=<boolean>

        Does not accept a slug combined with include_deleted, but does accept
        any other combination.
        """
        query_string = ""
        if kwargs:
            query_string = self._format_endpoints(kwargs)
            if query_string is None:
                error_message = "invalid combination: slug and include_deleted"
                return [{self.error: error_message}]

        # Construct query url - query_string is empty if no kwargs
        url = "{0}/projects{1}".format(self.baseurl, query_string)

        # Attempt to GET projects
        try:
            # Success!
            response = requests.get(url)
            return self._json_to_python(response.text)
        except requests.exceptions.RequestException as e:
            # Request Error
            return e

    def get_activities(self, **kwargs):
        """
        get_activities([kwargs])

        Request activity information filtered by parameters passed to
        ``kwargs``. Returns a list of python objects representing the JSON
        activity information returned by TimeSync or an error message if
        unsuccessful.

        ``kwargs`` contains the optional query parameters described in the
        TimeSync documentation. If ``kwargs`` is empty, ``get_activities()``
        will return all activities in the database. The syntax for each
        argument is ``query="parameter"`` or ``bool_query=<boolean>``.

        Optional parameters:
        slug="<slug>"
        include_deleted=<boolean>
        revisions=<boolean>

        Does not accept a slug combined with include_deleted, but does accept
        any other combination.
        """
        query_string = ""
        if kwargs:
            query_string = self._format_endpoints(kwargs)
            if query_string is None:
                error_message = "invalid combination: slug and include_deleted"
                return [{self.error: error_message}]

        # Construct query url - query_string is empty if no kwargs
        url = "{0}/activities{1}".format(self.baseurl, query_string)

        # Attempt to GET activities
        try:
            # Success!
            response = requests.get(url)
            return self._json_to_python(response.text)
        except requests.exceptions.RequestException as e:
            # Request Error
            return e

###############################################################################
# Internal methods
###############################################################################

    def _auth(self):
        """Returns auth object to be send to TimeSync"""
        return {"type": self.auth_type,
                "username": self.user,
                "password": self.password, }

    def _json_to_python(self, json_object):
        """Convert json object to native python list of objects"""
        python_object = json.loads(str(json_object))

        if not isinstance(python_object, list):
            python_object = [python_object]

        return python_object

    def _format_endpoints(self, queries):
        """Format endpoints for GET projects and activities requests"""
        query_string = ""
        query_list = []

        # The following combination is not allowed
        if "slug" in queries.keys() and "include_deleted" in queries.keys():
            return None
        # slug goes first, then delete it so it doesn't show up after the ?
        elif "slug" in queries.keys():
            query_string = "/{}".format(queries["slug"])
            del(queries["slug"])

        # Convert True and False booleans to TimeSync compatible strings
        for k, v in sorted(queries.items(), key=operator.itemgetter(0)):
            queries[k] = "true" if v else "false"
            query_list.append("{0}={1}".format(k, queries[k]))

        # Check for items in query_list after slug was removed, create
        # query string
        if query_list:
            query_string += "?{}".format("&".join(query_list))

        return query_string

    def _get_field_errors(self, actual, object_name, create_object):
        """Checks that ``actual`` parameter passed to POST method contains
        items in required or optional lists for that ``object_name``.
        Returns None if no errors found or error string if error found. If
        ``create_object`` then ``actual`` gets checked for required fields"""
        # Check that actual is a python dict
        if not isinstance(actual, dict):
            return "{} object: must be python dictionary".format(object_name)

        missing_list = list(self.required_params[object_name])

        for key in actual:
            if (key not in self.required_params[object_name]
                    and key not in self.optional_params[object_name]):
                return "{0} object: invalid field: {1}".format(object_name,
                                                               key)

            # Remove field from copied list if the field is in required
            if key in self.required_params[object_name]:
                del(missing_list[missing_list.index(key)])

        # If there is anything in missing_list, it is an absent required field
        if missing_list and create_object:
            return "{0} object: missing required field(s): {1}".format(
                object_name, ", ".join(missing_list))

        # No errors if we made it this far
        return None

    def _create_or_update(self, parameters, slug_or_uuid,
                          obj_name, endpoint, create_object=True):
        """
        Create or update an object ``obj_name`` at specified ``endpoint``. This
        method will return that object in the form of a list containing a
        single python dictionary. The dictionary will contain a representation
        of the JSON body returned by TimeSync if it was successful or error
        information if it was not. If ``create_object``, then ``parameters``
        gets checked for required fields.
        """
        # Check that parameter_dict contains required fields and no bad fields
        field_error = self._get_field_errors(parameters,
                                             obj_name,
                                             create_object)
        if field_error:
            return [{self.error: field_error}]

        values = {"auth": self._auth(), "object": parameters}

        slug_or_uuid = "/{}".format(slug_or_uuid) if slug_or_uuid else ""

        # Construct url to post to
        url = "{0}/{1}{2}".format(self.baseurl, endpoint, slug_or_uuid)

        # Attempt to POST to TimeSync
        try:
            # Success!
            response = requests.post(url, json=values)
            return self._json_to_python(response.text)
        except requests.exceptions.RequestException as e:
            # Request error
            return e
