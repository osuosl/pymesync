"""
pymesync - Python TimeSync Module

Allows for interactions with the TimeSync API

- authenticate(username, password, auth_type) - Authorizes user with TimeSync
- token_expiration_time() - Returns datetime expiration of user authentication
- create_time(time) - Sends time to baseurl (TimeSync)
- update_time(time, uuid) - Updates time by uuid
- create_project(project) - Creates project
- update_project(project, slug) - Updates project by slug
- create_activity(activity) - Creates activity
- update_activity(activity, slug) - Updates activity by slug
- create_user(user) - Creates a user
- update_user(user, username) - Updates user by username
- get_times(query_parameters) - Get times from TimeSync
- get_projects(query_parameters) - Get project information from TimeSync
- get_activities(query_parameters) - Get activity information from TimeSync
- get_users(username) - Get user information from TimeSync

Supported TimeSync versions:
v1
"""
import json
import requests
import operator
import base64
import ast
import datetime
import mock_pymesync
import time
import bcrypt


class TimeSync(object):

    def __init__(self, baseurl, token=None, test=False):
        self.baseurl = baseurl[:-1] if baseurl.endswith("/") else baseurl
        self.user = None
        self.password = None
        self.auth_type = None
        self.token = token
        self.error = "pymesync error"
        self.test = test
        self.valid_get_queries = ["user", "project", "activity",
                                  "start", "end", "include_revisions",
                                  "include_deleted", "uuid"]
        self.required_params = {
            "time":     ["duration", "project", "user", "date_worked"],
            "project":  ["name", "slugs"],
            "activity": ["name", "slug"],
            "user":     ["username", "password"],
        }
        self.optional_params = {
            "time":     ["notes", "issue_uri", "activities"],
            "project":  ["uri", "users", "default_activity"],
            "activity": [],
            "user":     ["display_name", "email", "site_admin",
                         "site_spectator", "site_manager", "meta", "active"],
        }

    def authenticate(self, username=None, password=None, auth_type=None):
        """
        authenticate(username, password, auth_type)

        Authenticate a username and password with TimeSync via a POST request
        to the login endpoint. This method will return a list containing a
        single python dictionary. If successful, the dictionary will contain
        the token in the form [{"token": "SOMETOKEN"}]. If an error is returned
        the dictionary will contain the error information.

        ``username`` is a string containing the username of the TimeSync user
        ``password`` is a string containing the user's password
        ``auth_type`` is a string containing the authentication method used by
        TimeSync
        """
        # Check for correct arguments in method call
        arg_error_list = []
        if not username:
            arg_error_list.append("username")

        if not password:
            arg_error_list.append("password")

        if not auth_type:
            arg_error_list.append("auth_type")

        if arg_error_list:
            return {self.error: "Missing {}; "
                                "please add to method call".format(
                                    ", ".join(arg_error_list))}

        del(arg_error_list)

        self.user = username
        self.password = password
        self.auth_type = auth_type

        # Create the auth block to send to the login endpoint
        auth = {"auth": self.__auth()}

        # Construct the url with the login endpoint
        url = "{}/login".format(self.baseurl)

        # Test mode, set self.token and return it from the mocked method
        if self.test:
            self.token = "TESTTOKEN"
            return mock_pymesync.authenticate()

        # Send the request, then convert the resonse to a python dictionary
        try:
            # Success!
            response = requests.post(url, json=auth)
            token_response = self.__response_to_python(response)
        except requests.exceptions.RequestException as e:
            # Request error
            return {self.error: e}

        # If TimeSync returns an error, return the error without setting the
        # token.
        # Else set the token to the returned token and return the dict.
        if "error" in token_response or "token" not in token_response:
            return token_response
        else:
            self.token = token_response["token"]
            return token_response

    def create_time(self, time):
        """
        create_time(time)

        Send a time entry to TimeSync via a POST request in a JSON body. This
        method will return that body in the form of a list containing a single
        python dictionary. The dictionary will contain a representation of that
        JSON body if it was successful or error information if it was not.

        ``time`` is a python dictionary containing the time information to send
        to TimeSync.
        """
        if time['duration'] < 0:
            return {self.error: "time object: duration cannot be negative"}

        if not isinstance(time['duration'], int):
            duration = self.__duration_to_seconds(time['duration'])
            time['duration'] = duration

            # Duration at this point contains an error_msg if it's not an int
            if not isinstance(time['duration'], int):
                return duration

        return self.__create_or_update(time, None, "time", "times")

    def update_time(self, time, uuid):
        """
        update_time(time, uuid)

        Send a time entry update to TimeSync via a POST request in a JSON body.
        This method will return that body in the form of a list containing a
        single python dictionary. The dictionary will contain a representation
        of that updated time object if it was successful or error information
        if it was not.

        ``time`` is a python dictionary containing the time information to send
        to TimeSync.
        ``uuid`` contains the uuid for a time entry to update.
        """
        if time['duration'] < 0:
            return {self.error: "time object: duration cannot be negative"}

        if not isinstance(time['duration'], int):
            duration = self.__duration_to_seconds(time['duration'])
            time['duration'] = duration

            # Duration at this point contains an error_msg if it's not an int
            if not isinstance(time['duration'], int):
                return duration

        return self.__create_or_update(time, uuid, "time", "times", False)

    def create_project(self, project):
        """
        create_project(project)

        Post a project to TimeSync via a POST request in a JSON body. This
        method will return that body in the form of a list containing a single
        python dictionary. The dictionary will contain a representation of that
        JSON body if it was successful or error information if it was not.

        ``project`` is a python dictionary containing the project information
        to send to TimeSync.
        """
        return self.__create_or_update(project, None, "project", "projects")

    def update_project(self, project, slug):
        """
        update_project(project, slug)

        Send a project update to TimeSync via a POST request in a JSON body.
        This method will return that body in the form of a list containing a
        single python dictionary. The dictionary will contain a representation
        of that updated project object if it was successful or error
        information if it was not.

        ``project`` is a python dictionary containing the project information
        to send to TimeSync.
        ``slug`` contains the slug for a project entry to update.
        """
        return self.__create_or_update(project, slug, "project", "projects",
                                       False)

    def create_activity(self, activity):
        """
        create_activity(activity, slug=None)

        Post an activity to TimeSync via a POST request in a JSON body. This
        method will return that body in the form of a list containing a single
        python dictionary. The dictionary will contain a representation of that
        JSON body if it was successful or error information if it was not.

        ``activity`` is a python dictionary containing the activity information
        to send to TimeSync.
        """
        return self.__create_or_update(activity, None,
                                       "activity", "activities")

    def update_activity(self, activity, slug):
        """
        update_activity(activity, slug)

        Send an activity update to TimeSync via a POST request in a JSON body.
        This method will return that body in the form of a list containing a
        single python dictionary. The dictionary will contain a representation
        of that updated activity object if it was successful or error
        information if it was not.

        ``activity`` is a python dictionary containing the project information
        to send to TimeSync.
        ``slug`` contains the slug for an activity entry to update.
        """
        return self.__create_or_update(activity, slug,
                                       "activity", "activities",
                                       False)

    def create_user(self, user):
        """
        create_user(user)

        Post a user to TimeSync via a POST request in a JSON body. This
        method will return that body in the form of a list containing a single
        python dictionary. The dictionary will contain a representation of that
        JSON body if it was successful or error information if it was not.

        ``user`` is a python dictionary containing the user information to send
        to TimeSync.
        """
        for perm in ["site_admin", "site_manager", "site_spectator", "active"]:
            if perm in user and not isinstance(user[perm], bool):
                return {self.error: "user object: "
                        "{} must be True or False".format(perm)}

        # Only hash password if it is present
        # Don't error out here so that internal methods can catch all missing
        # fields later on and return a more meaningful error if necessary.
        if "password" in user:
            # Hash the password
            password = user["password"]
            hashed = bcrypt.hashpw(password, bcrypt.gensalt(prefix=b"2a",
                                                            rounds=10))
            user["password"] = hashed

        return self.__create_or_update(user, None, "user", "users")

    def update_user(self, user, username):
        """
        update_user(user, username)

        Send a user update to TimeSync via a POST request in a JSON body.
        This method will return that body in the form of a list containing a
        single python dictionary. The dictionary will contain a representation
        of that updated user object if it was successful or error
        information if it was not.

        ``user`` is a python dictionary containing the user information to send
        to TimeSync.
        ``username`` contains the username for a user to update.
        """
        for perm in ["site_admin", "site_manager", "site_spectator", "active"]:
            if perm in user and not isinstance(user[perm], bool):
                return {self.error: "user object: "
                        "{} must be True or False".format(perm)}

        # Only hash password if it is present
        # Don't error out here so that internal methods can catch all missing
        # fields later on and return a more meaningful error if necessary.
        if "password" in user:
            # Hash the password
            password = user["password"]
            hashed = bcrypt.hashpw(password, bcrypt.gensalt(prefix=b"2a",
                                                            rounds=10))
            user["password"] = hashed

        return self.__create_or_update(user, username, "user", "users", False)

    def get_times(self, query_parameters=None):
        """
        get_times(query_parameters)

        Request time entries filtered by parameters passed in
        ``query_parameters``. Returns a list of python objects representing the
        JSON time information returned by TimeSync or an error message if
        unsuccessful.

        ``query_parameters`` is a python dictionary containing the optional
        query parameters described in the TimeSync documentation. If
        ``query_parameters`` is empty or None, ``get_times()`` will return all
        times in the database. The syntax for each argument is
        ``{"query": ["parameter"]}``.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return [{self.error: local_auth_error}]

        # Check for key error
        if query_parameters:
            for key in query_parameters:
                if key not in self.valid_get_queries:
                    return [{self.error: "invalid query: {}".format(key)}]

        # Initialize the query string
        query_string = ""

        # If there are filtering parameters, construct them correctly.
        # Else reinitialize the query string to a ? so we can add the token.
        if query_parameters:
            query_string = self.__construct_filter_query(query_parameters)
        else:
            query_string = "?"

        # Construct query url, at this point query_string ends with a ?
        url = "{0}/times{1}token={2}".format(self.baseurl,
                                             query_string,
                                             self.token)

        # Test mode, return one or many objects depending on if uuid is passed
        if self.test:
            if query_parameters and "uuid" in query_parameters:
                return mock_pymesync.get_times(query_parameters["uuid"])
            else:
                return mock_pymesync.get_times(None)

        # Attempt to GET times, then convert the response to a python
        # dictionary
        try:
            # Success!
            response = requests.get(url)
            return self.__response_to_python(response)
        except requests.exceptions.RequestException as e:
            # Request Error
            return [{self.error: e}]

    def get_projects(self, query_parameters=None):
        """
        get_projects(query_parameters)

        Request project information filtered by parameters passed to
        ``query_parameters``. Returns a list of python objects representing the
        JSON project information returned by TimeSync or an error message if
        unsuccessful.

        ``query_parameters`` is a python dict containing the optional query
        parameters described in the TimeSync documentation. If
        ``query_parameters`` is empty or None, ``get_projects()`` will return
        all projects in the database. The syntax for each argument is
        ``{"query": "parameter"}`` or ``{"bool_query": <boolean>}``.

        Optional parameters:
        "slug": "<slug>"
        "include_deleted": <boolean>
        "revisions": <boolean>

        Does not accept a slug combined with include_deleted, but does accept
        any other combination.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return [{self.error: local_auth_error}]

        # Save for passing to test mode since __format_endpoints deletes
        # kwargs["slug"] if it exists
        if query_parameters and "slug" in query_parameters:
            slug = query_parameters["slug"]
        else:
            slug = None

        query_string = ""

        # If kwargs exist, create a correct query string
        # Else, prepare query_string for the token
        if query_parameters:
            query_string = self.__format_endpoints(query_parameters)
            # If __format_endpoints returns None, it was passed both slug and
            # include_deleted, which is not allowed by the TimeSync API
            if query_string is None:
                error_message = "invalid combination: slug and include_deleted"
                return [{self.error: error_message}]
        else:
            query_string = "?token={}".format(self.token)

        # Construct query url - at this point query_string ends with
        # ?token=self.token
        url = "{0}/projects{1}".format(self.baseurl, query_string)

        # Test mode, return list of projects if slug is None, or a single
        # project
        if self.test:
            return mock_pymesync.get_projects(slug)

        # Attempt to GET projects, then convert the response to a python
        # dictionary
        try:
            # Success!
            response = requests.get(url)
            return self.__response_to_python(response)
        except requests.exceptions.RequestException as e:
            # Request Error
            return [{self.error: e}]

    def get_activities(self, query_parameters=None):
        """
        get_activities(query_parameters)

        Request activity information filtered by parameters passed to
        ``query_parameters``. Returns a list of python objects representing
        the JSON activity information returned by TimeSync or an error message
        if unsuccessful.

        ``query_parameters`` is a dictionary containing the optional query
        parameters described in the TimeSync documentation. If
        ``query_parameters`` is empty or None, ``get_activities()`` will
        return all activities in the database. The syntax for each argument is
        ``{"query": "parameter"}`` or ``{"bool_query": <boolean>}``.

        Optional parameters:
        "slug": "<slug>"
        "include_deleted": <boolean>
        "revisions": <boolean>

        Does not accept a slug combined with include_deleted, but does accept
        any other combination.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return [{self.error: local_auth_error}]

        # Save for passing to test mode since __format_endpoints deletes
        # kwargs["slug"] if it exists
        if query_parameters and "slug" in query_parameters:
            slug = query_parameters["slug"]
        else:
            slug = None

        query_string = ""

        # If kwargs exist, create a correct query string
        # Else, prepare query_string for the token
        if query_parameters:
            query_string = self.__format_endpoints(query_parameters)
            # If __format_endpoints returns None, it was passed both slug and
            # include_deleted, which is not allowed by the TimeSync API
            if query_string is None:
                error_message = "invalid combination: slug and include_deleted"
                return [{self.error: error_message}]
        else:
            query_string = "?token={}".format(self.token)

        # Construct query url - at this point query_string ends with
        # ?token=self.token
        url = "{0}/activities{1}".format(self.baseurl, query_string)

        # Test mode, return list of projects if slug is None, or a list of
        # projects
        if self.test:
            return mock_pymesync.get_activities(slug)

        # Attempt to GET activities, then convert the response to a python
        # dictionary
        try:
            # Success!
            response = requests.get(url)
            return self.__response_to_python(response)
        except requests.exceptions.RequestException as e:
            # Request Error
            return [{self.error: e}]

    def get_users(self, username=None):
        """
        get_users(username=None)

        Request user entities from the TimeSync instance specified by the
        baseurl provided when instantiating the TimeSync object. Returns a list
        of python dictionaries containing the user information returned by
        TimeSync or an error message if unsuccessful.

        ``username`` is an optional parameter containing a string of the
        specific username to be retrieved. If ``username`` is not provided, a
        list containing all users will be returned. Defaults to ``None``.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return [{self.error: local_auth_error}]

        # url should end with /users if no username is passed else
        # /users/username
        url = "{0}/users/{1}".format(self.baseurl, username) if username else (
              "{}/users".format(self.baseurl))

        # The url should always end with a token
        url += "?token={}".format(self.token)

        # Test mode, return one user object if username is passed else return
        # several user objects
        if self.test:
            return mock_pymesync.get_users(username)

        # Attempt to GET users, then convert the response to a python
        # dictionary
        try:
            # Success!
            response = requests.get(url)
            return self.__response_to_python(response)
        except requests.exceptions.RequestException as e:
            # Request Error
            return [{self.error: e}]

    def delete_time(self, uuid=None):
        """
        delete_time(uuid=None)

        Allows the currently authenticated user to delete their own time entry
        by uuid.

        ``uuid`` is a string containing the uuid of the time entry to be
        deleted.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return {self.error: local_auth_error}

        if not uuid:
            return {self.error: "missing uuid; please add to method call"}

        return self.__delete_object("times", uuid)

    def delete_project(self, slug=None):
        """
        delete_project(slug=None)

        Allows the currently authenticated admin user to delete a project
        record by slug.

        ``slug`` is a string containing the slug of the project to be deleted.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return {self.error: local_auth_error}

        if not slug:
            return {self.error: "missing slug; please add to method call"}

        return self.__delete_object("projects", slug)

    def delete_activity(self, slug=None):
        """
        delete_activity(slug=None)

        Allows the currently authenticated admin user to delete an activity
        record by slug.

        ``slug`` is a string containing the slug of the activity to be deleted.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return {self.error: local_auth_error}

        if not slug:
            return {self.error: "missing slug; please add to method call"}

        return self.__delete_object("activities", slug)

    def delete_user(self, username=None):
        """
        delete_user(username=None)

        Allows the currently authenticated admin user to delete a user
        record by username.

        ``username`` is a string containing the username of the user to be
        deleted.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return {self.error: local_auth_error}

        if not username:
            return {self.error:
                    "missing username; please add to method call"}

        return self.__delete_object("users", username)

    def token_expiration_time(self):
        """
        token_expiration_time()

        Returns the expiration time of the JWT (JSON Web Token) associated with
        this object.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return {self.error: local_auth_error}

        # Return valid date if in test mode
        if self.test:
            return mock_pymesync.token_expiration_time()

        # Decode the token, then get the second dict (payload) from the
        # resulting string. The payload contains the expiration time.
        try:
            decoded_payload = base64.b64decode(self.token.split(".")[1])
        except:
            return {self.error: "improperly encoded token"}

        # literal_eval the string representation of a dict to convert it to a
        # dict, then get the value at 'exp'. The value at 'exp' is epoch time
        # in ms
        exp_int = ast.literal_eval(decoded_payload)['exp']

        # Convert the epoch time from ms to s
        exp_int /= 1000

        # Convert and format the epoch time to python datetime.
        exp_datetime = datetime.datetime.fromtimestamp(exp_int)

        return exp_datetime

    def project_users(self, project=None):
        """
        project_users(project)

        Returns a dict of users for the specified project containing usernames
        mapped to their list of permissions for the project.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return {self.error: local_auth_error}

        # Check that a project slug was passed
        if not project:
            return {self.error: "Missing project slug, please "
                                "include in method call"}

        # Construct query url
        url = "{0}/projects/{1}?token={2}".format(self.baseurl,
                                                  project,
                                                  self.token)
        # Return valid user object if in test mode
        if self.test:
            return mock_pymesync.project_users()

        # Try to get the project object
        try:
            # Success!
            response = requests.get(url)
            project_object = self.__response_to_python(response)
        except requests.exceptions.RequestException as e:
            # Request Error
            return {self.error: e}

        # Create the user dict to return
        # There was an error, don't do anything with it, return as a list
        if "error" in project_object:
            return project_object

        # Get the user object from the project
        users = project_object["users"]

        # Convert the nested permissions dict to a list containing only
        # relevant (true) permissions
        for user in users:
            perm = []
            for permission in users[user]:
                if users[user][permission] is True:
                    perm.append(permission)
            users[user] = perm

        return users

###############################################################################
# Internal methods
###############################################################################

    def __auth(self):
        """Returns auth object to log in to TimeSync"""
        return {"type": self.auth_type,
                "username": self.user,
                "password": self.password, }

    def __token_auth(self):
        """Returns auth object with a token to send to TimeSync endpoints"""
        return {"type": "token",
                "token": self.token, }

    def __local_auth_error(self):
        """Checks that self.token is set. Returns error if not set, otherwise
        returns None"""
        return None if self.token else ("Not authenticated with TimeSync, "
                                        "call self.authenticate() first")

    def __response_to_python(self, response):
        """Convert response to native python list of objects"""
        # DELETE returns an empty body if successful
        if not response.text and response.status_code == 200:
            return {"status": 200}

        # If response.text is valid JSON, it came from TimeSync. If it isn't
        # and we got a ValueError, we know we are having trouble connecting to
        # TimeSync because we are not getting a return from TimeSync.
        try:
            python_object = json.loads(unicode(response.text))
        except ValueError:
            # If we get a ValueError, response.text isn't a JSON object, and
            # therefore didn't come from a TimeSync connection.
            err_msg = "connection to TimeSync failed at baseurl {} - ".format(
                self.baseurl)
            err_msg += "response status was {}".format(response.status_code)
            return {self.error: err_msg}

        return python_object

    def __format_endpoints(self, queries):
        """Format endpoints for GET projects and activities requests. Returns
        None if invalid combination of slug and include_deleted"""
        query_string = "?"
        query_list = []

        # The following combination is not allowed
        if "slug" in queries and "include_deleted" in queries:
            return None
        # slug goes first, then delete it so it doesn't show up after the ?
        elif "slug" in queries:
            query_string = "/{}?".format(queries["slug"])
            del(queries["slug"])

        # Convert True and False booleans to TimeSync compatible strings
        for k, v in sorted(queries.items(), key=operator.itemgetter(0)):
            queries[k] = "true" if v else "false"
            query_list.append("{0}={1}".format(k, queries[k]))

        # Check for items in query_list after slug was removed, create
        # query string
        if query_list:
            query_string += "{}&".format("&".join(query_list))

        # Authenticate and return
        query_string += "token={}".format(self.token)

        return query_string

    def __construct_filter_query(self, queries):
        """Construct the query string for filtering GET queries, such as
        get_times()"""
        query_string = "?"
        query_list = []

        # Format the include_* queries similarly to other queries for easier
        # processing
        if "include_deleted" in queries.keys():
            queries["include_deleted"] = (["true"]
                                          if queries["include_deleted"]
                                          else ["false"])

        if "include_revisions" in queries.keys():
            queries["include_revisions"] = (["true"]
                                            if queries["include_revisions"]
                                            else ["false"])

        # If uuid is included, the only other accepted queries are the
        # include_*s
        if "uuid" in queries.keys():
            query_string = "/{}?".format(queries["uuid"])
            if "include_deleted" in queries.keys():
                query_string += "include_deleted={}&".format(
                    queries["include_deleted"][0])
            if "include_revisions" in queries.keys():
                query_string += "include_revisions={}&".format(
                    queries["include_revisions"][0])

        # Everthing is a list now, so iterate through and append
        else:
            # Sort them into an alphabetized list for easier testing
            sorted_qs = sorted(queries.items(), key=operator.itemgetter(0))
            for query, param in sorted_qs:
                for slug in param:
                    # Format each query in the list
                    query_list.append("{0}={1}".format(query, slug))

            # Construct the query_string using the list.
            # Last character will be an & so we can append the token
            for string in query_list:
                query_string += "{}&".format(string)

        return query_string

    def __get_field_errors(self, actual, object_name, create_object):
        """Checks that ``actual`` parameter passed to POST method contains
        items in required or optional lists for that ``object_name``.
        Returns None if no errors found or error string if error found. If
        ``create_object`` then ``actual`` gets checked for required fields"""
        # Check that actual is a python dict
        if not isinstance(actual, dict):
            return "{} object: must be python dictionary".format(object_name)

        # missing_list contains a list of all the required parameters that were
        # not passed. It is initialized to all required parameters.
        missing_list = list(self.required_params[object_name])

        # For each key, if it is not required or optional, it is not allowed
        # If it is requried, remove that parameter from the missing_list, since
        # it is no longer missing
        for key in actual:
            if (key not in self.required_params[object_name]
                    and key not in self.optional_params[object_name]):
                return "{0} object: invalid field: {1}".format(object_name,
                                                               key)

            # Remove field from copied list if the field is in required
            if key in self.required_params[object_name]:
                del(missing_list[missing_list.index(key)])

        # If there is anything in missing_list, it is an absent required field
        # This only needs to be checked if the create_object flag is passed
        if create_object and missing_list:
            return "{0} object: missing required field(s): {1}".format(
                object_name, ", ".join(missing_list))

        # No errors if we made it this far
        return None

    def __create_or_update(self, object_fields, identifier,
                           object_name, endpoint, create_object=True):
        """
        Create or update an object ``object_name`` at specified ``endpoint``.
        This method will return that object in the form of a list containing a
        single python dictionary. The dictionary will contain a representation
        of the JSON body returned by TimeSync if it was successful or error
        information if it was not. If ``create_object``, then ``parameters``
        gets checked for required fields.
        """
        # Check that user has authenticated
        local_auth_error = self.__local_auth_error()
        if local_auth_error:
            return {self.error: local_auth_error}

        # Check that object contains required fields and no bad fields
        field_error = self.__get_field_errors(object_fields,
                                              object_name,
                                              create_object)
        if field_error:
            return {self.error: field_error}

        # Since this is a POST request, we need an auth and object objects
        values = {"auth": self.__token_auth(), "object": object_fields}

        # Reformat the identifier with the leading '/' so it can be added to
        # the url. Do this here instead of the url assignment below so we can
        # set it to "" if it wasn't passed.
        identifier = "/{}".format(identifier) if identifier else ""

        # Construct url to post to
        url = "{0}/{1}{2}".format(self.baseurl, endpoint, identifier)

        # Test mode, remove leading '/' from identifier
        if self.test:
            return self.__test_handler(object_fields, identifier[1:],
                                       object_name, create_object)

        # Attempt to POST to TimeSync, then convert the response to a python
        # dictionary
        try:
            # Success!
            response = requests.post(url, json=values)
            return self.__response_to_python(response)
        except requests.exceptions.RequestException as e:
            # Request error
            return {self.error: e}

    def __duration_to_seconds(self, duration):
        """When a time_entry is created, a user will enter a time duration as
           one of the parameters of the object. This method will convert that
           entry (if it's entered as a string) into the appropriate integer
           equivalent (in seconds).
        """
        try:
            t = time.strptime(duration, "%Hh%Mm")
            hours_spent = t.tm_hour
            minutes_spent = t.tm_min

            # Convert duration to seconds
            return (hours_spent * 3600) + (minutes_spent * 60)
        except:
            error_msg = [{self.error: "time object: invalid duration string"}]
            return error_msg

    def __delete_object(self, endpoint, identifier):
        """Deletes object at ``endpoint`` identified by ``identifier``"""
        # Construct url
        url = "{0}/{1}/{2}?token={3}".format(self.baseurl,
                                             endpoint,
                                             identifier,
                                             self.token)

        # Test mode
        if self.test:
            return mock_pymesync.delete_object()

        # Attempt to DELETE object
        try:
            # Success!
            response = requests.delete(url)
            return self.__response_to_python(response)
        except requests.exceptions.RequestException as e:
            # Request error
            return {self.error: e}

    def __test_handler(self, parameters, identifier, obj_name, create_object):
        """Handle test methods in test mode for creating or updating an
        object"""
        # Man I wish python had a switch statement
        if obj_name == "time":
            if create_object:
                return mock_pymesync.create_time(parameters)
            else:
                return mock_pymesync.update_time(parameters, identifier)
        elif obj_name == "project":
            if create_object:
                return mock_pymesync.create_project(parameters)
            else:
                return mock_pymesync.update_project(parameters, identifier)
        elif obj_name == "activity":
            if create_object:
                return mock_pymesync.create_activity(parameters)
            else:
                return mock_pymesync.update_activity(parameters, identifier)
        elif obj_name == "user":
            if create_object:
                return mock_pymesync.create_user(parameters)
            else:
                return mock_pymesync.update_user(parameters, identifier)
