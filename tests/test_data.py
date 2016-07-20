class TestData():

    def __init__(self, data_in=None, data_out=None):
        self.data_in = data_in
        self.data_out = data_out

create_or_update_test_time = {
    "duration": 12,
    "project": "ganeti-web-manager",
    "user": "example-user",
    "activities": ["documenting"],
    "notes": "Worked on docs",
    "issue_uri": "https://github.com/",
    "date_worked": "2014-04-17"
}

create_or_update_test_user = {
    "username": "example-user",
    "password": "password",
    "display_name": "Example User",
    "email": "example.user@example.com",
    "site_admin": True,
    "site_spectator": False,
    "site_manager": False,
    "active": True
}

create_or_update_test_project = {
    "uri": "https://code.osuosl.org/projects/timesync",
    "name": "TimeSync API",
    "slugs": ["timesync", "time"],
    "users": {
        "mrsj": {"member": True, "spectator": True, "manager": True},
        "thai": {"member": True, "spectator": False, "manager": False}
    }
}

create_or_update_test_activity = {
    "name": "Quality Assurance/Testing",
    "slug": "qa"
}

test_tokenauth = {
    "type": "token",
    "token": "TESTTOKEN"
}

test_passauth = {
    "type": "password",
    "username": "example-user",
    "password": "password"
}

test_uuid = "sadfasdg432"

create_or_update_create_time_valid_data = TestData(
    data_in=[
        dict(create_or_update_test_time),  # time
        None,  # identifier
        "time",  # object_name
        "times"  # endpoint
    ],
    data_out=[
        [  # *args
            "http://ts.example.com/v1/times"
        ],
        {  # **kwargs
            "json": {
                "auth": dict(test_tokenauth),
                "object": dict(create_or_update_test_time)
            }
        }
    ]
)

create_or_update_update_time_valid_data = TestData(
    data_in=[
        dict(create_or_update_test_time),  # time
        "1234-5678-90abc-d",  # UUID
        "time",  # object_name
        "times"  # endpoint
    ],
    data_out=[
        [  # *args
            "http://ts.example.com/v1/times/1234-5678-90abc-d"
        ],
        {  # **kwargs
            "json": {
                "auth": dict(test_tokenauth),
                "object": dict(create_or_update_test_time)
            }
        }
    ]
)

create_or_update_update_time_valid_less_fields_data = TestData(
    data_in=[
        {"duration": 12},  # time
        "1234-5678-90abc-d", # UUID
        "time",  # object_name
        "times",  # endpoint
        False  # create_object
    ],
    data_out=[
        [  # *args
            "http://ts.example.com/v1/times/1234-5678-90abc-d"
        ],
        {  # **kwargs
            "json": {
                "auth": dict(test_tokenauth),
                "object": {"duration": 12}
            }
        }
    ]
)

create_or_update_create_time_invalid_data = TestData(
    data_in=[
        dict(create_or_update_test_time.items() + [("bad", "field")]),  # time
        None,  # UUID
        "time",  # object_name
        "times"  # endpoint
    ]
)

create_or_update_create_time_two_required_missing_data = TestData(
    data_in=[
        {  # time
            "user": "example-user",
            "notes": "Worked on docs",
            "issue_uri": "https://github.com/",
            "date_worked": "2014-04-17"
        },
        None,  # UUID
        "time",  # object_name
        "times"  # endpoint
    ]
)

create_or_update_create_time_each_required_missing_data = TestData(
    data_in=[
        {  # time
            "duration": 12,
            "project": "ganeti-web-manager",
            "user": "example-user",
            "date_worked": "2014-04-17"
        },
        None,  # UUID
        "time",  # object_name
        "times"  # endpoint
    ]
)

create_or_update_create_time_type_error_data = TestData(
    data_in=[
        [  # "time"
            1,
            "hello",
            [1, 2, 3],
            None,
            True,
            False,
            1.234
        ],
        None,
        "time",
        "times"
    ]
)

create_or_update_create_user_valid_data = TestData(
    data_in=[
        dict(create_or_update_test_user),
        None,
        "user",
        "users"
    ],
    data_out=[
        [
            "http://ts.example.com/v1/users"
        ],
        {
            "json": {
                "auth": dict(test_tokenauth),
                "object": dict(create_or_update_test_user)
            }
        }
    ]
)

create_or_update_update_user_valid_data = TestData(
    data_in=[
        dict(create_or_update_test_user),
        "example-user",
        "user",
        "users"
    ],
    data_out=[
        [
            "http://ts.example.com/v1/users/example-user"
        ],
        {
            "json": {
                "auth": dict(test_tokenauth),
                "object": dict(create_or_update_test_user)
            }
        }
    ]
)

create_or_update_update_user_valid_less_fields_data = TestData(
    data_in=[
        {"display_name": "Example User"},
        "example-user",
        "user",
        "users",
        False
    ],
    data_out=[
        [
            "http://ts.example.com/v1/users/example-user"
        ],
        {
            "json": {
                "auth": dict(test_tokenauth),
                "object": {"display_name": "Example User"}
            }
        }
    ]
)

create_or_update_create_user_invalid_data = TestData(
    data_in=[
        dict(create_or_update_test_user.items() + [("bad", "field")]),
        None,
        "user",
        "users"
    ]
)

create_or_update_create_user_two_required_missing_data = TestData(
    data_in=[
        {
            "display_name": "Example User",
            "email": "example.user@example.com"
        },
        None,
        "user",
        "users"
    ],
)

create_or_update_create_user_each_required_missing_data = TestData(
    data_in=[
        {
            "username": "example-user",
            "password": "password"
        },
        None,
        "user",
        "users"
    ]
)

create_or_update_create_user_type_error_data = TestData(
    data_in=[
        [  # "user"
            1,
            "hello",
            [1, 2, 3],
            None,
            True,
            False,
            1.234
        ],
        None,
        "user",
        "users"
    ]
)

create_or_update_create_project_valid_data = TestData(
    data_in=[
        dict(create_or_update_test_project),
        None,
        "project",
        "projects"
    ],
    data_out=[
        [
            "http://ts.example.com/v1/projects"
        ],
        {
            "json": {
                "auth": dict(test_tokenauth),
                "object": dict(create_or_update_test_project)
            }
        }
    ]
)

create_or_update_update_project_valid_data = TestData(
    data_in=[
        dict(create_or_update_test_project),
        "slug",
        "project",
        "projects"
    ],
    data_out=[
        [
            "http://ts.example.com/v1/projects/slug"
        ],
        {
            "json": {
                "auth": dict(test_tokenauth),
                "object": dict(create_or_update_test_project)
            }
        }
    ]
)

create_or_update_update_project_valid_less_fields_data = TestData(
    data_in=[
        {"slugs": ["timesync", "time"]},
        "slug",
        "project",
        "projects",
        False
    ],
    data_out=[
        [
            "http://ts.example.com/v1/projects/slug"
        ],
        {
            "json": {
                "auth": dict(test_tokenauth),
                "object": {"slugs": ["timesync", "time"]}
            }
        }
    ]
)

create_or_update_create_project_invalid_data = TestData(
    data_in=[
        dict(create_or_update_test_project.items() + [("bad", "field")]),
        None,
        "project",
        "projects"
    ]
)

create_or_update_create_project_required_missing_data = TestData(
    data_in=[
        {"slugs": ["timesync", "time"]},
        None,
        "project",
        "projects"
    ]
)

create_or_update_create_project_each_required_missing_data = TestData(
    data_in=[
        {
            "name": "TimeSync API",
            "slugs": ["timesync", "time"]
        },
        None,
        "project",
        "projects"
    ]
)

create_or_update_create_project_type_error_data = TestData(
    data_in=[
        [  # "project"
            1,
            "hello",
            [1, 2, 3],
            None,
            True,
            False,
            1.234
        ],
        None,
        "project",
        "projects"
    ]
)

create_or_update_create_activity_valid_data = TestData(
    data_in=[
        dict(create_or_update_test_activity),
        None,
        "activity",
        "activities"
    ],
    data_out=[
        [
            "http://ts.example.com/v1/activities"
        ],
        {
            "json": {
                "auth": dict(test_tokenauth),
                "object": dict(create_or_update_test_activity)
            }
        }
    ]
)

create_or_update_update_activity_valid_data = TestData(
    data_in=[
        dict(create_or_update_test_activity),
        "slug",
        "activity",
        "activities"
    ],
    data_out=[
        [
            "http://ts.example.com/v1/activities/slug"
        ],
        {
            "json": {
                "auth": dict(test_tokenauth),
                "object": dict(create_or_update_test_activity)
            }
        }
    ]
)

create_or_update_update_activity_valid_less_fields_data = TestData(
    data_in=[
        {"slug": "qa"},
        "slug",
        "activity",
        "activities",
        False
    ],
    data_out=[
        [
            "http://ts.example.com/v1/activities/slug"
        ],
        {
            "json": {
                "auth": dict(test_tokenauth),
                "object": {"slug": "qa"}
            }
        }
    ]
)

create_or_update_create_activity_invalid_data = TestData(
    data_in=[
        dict(create_or_update_test_activity.items() + [("bad", "field")]),
        None,
        "activity",
        "activities"
    ]
)

create_or_update_create_activity_required_missing_data = TestData(
    data_in=[
        {"name": "Quality Assurance/Testing"},
        None,
        "activity",
        "activities"
    ]
)

create_or_update_create_activity_each_required_missing_data = TestData(
    data_in=[
        dict(create_or_update_test_activity),
        None,
        "activity",
        "activities"
    ]
)

create_or_update_create_activity_type_error_data = TestData(
    data_in=[
        [  # "activity"
            1,
            "hello",
            [1, 2, 3],
            None,
            True,
            False,
            1.234
        ],
        None,
        "activity",
        "activities"
    ]
)

create_or_update_create_time_no_auth_data = TestData(
    data_in=[
        dict(create_or_update_test_time),
        None,
        "time",
        "times"
    ]
)

create_or_update_create_user_no_auth_data = TestData(
    data_in=[
        dict(create_or_update_test_user),
        None,
        "user",
        "user"
    ]
)

create_or_update_create_project_no_auth_data = TestData(
    data_in=[
        dict(create_or_update_test_project),
        None,
        "project",
        "projects"
    ]
)

create_or_update_create_activity_no_auth_data = TestData(
    data_in=[
        dict(create_or_update_test_activity),
        None,
        "activity",
        "activities"
    ]
)

create_or_update_update_time_no_auth_data = TestData(
    data_in=[
        dict(create_or_update_test_time),
        None,
        "time",
        "times"
    ]
)

create_or_update_update_user_no_auth_data = TestData(
    data_in=[
        dict(create_or_update_test_user),
        None,
        "user",
        "user"
    ]
)

create_or_update_update_project_no_auth_data = TestData(
    data_in=[
        dict(create_or_update_test_project),
        None,
        "project",
        "projects"
    ]
)

create_or_update_update_activity_no_auth_data = TestData(
    data_in=[
        dict(create_or_update_test_activity),
        None,
        "activity",
        "activities"
    ]
)

auth_data = TestData(
    data_out=dict(test_passauth)
)

get_time_for_user_data = TestData(
    data_in={"user": ["example-user"]},
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?user=example-user&token=TESTTOKEN"
    ]
)

get_time_for_proj_data = TestData(
    data_in={"project": ["gwm"]},
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?project=gwm&token=TESTTOKEN"
    ]
)

get_time_for_activity_data = TestData(
    data_in={"activity": ["dev"]},
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?activity=dev&token=TESTTOKEN"
    ]
)

get_time_for_start_date_data = TestData(
    data_in={"start": ["2016-01-01"]},
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?start=2016-01-01&token=TESTTOKEN"
    ]
)

get_time_for_end_date_data = TestData(
    data_in={"end": ["2016-05-04"]},
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?end=2016-05-04&token=TESTTOKEN"
    ]
)

get_time_for_include_revisions_data = TestData(
    data_in={"include_revisions": True},
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?include_revisions=true&token=TESTTOKEN"
    ]
)

get_time_for_include_revisions_false_data = TestData(
    data_in={"include_revisions": False},
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?include_revisions=false&token=TESTTOKEN"
    ]
)

get_time_for_include_deleted_data = TestData(
    data_in={"include_deleted": True},
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?include_deleted=true&token=TESTTOKEN"
    ]
)

get_time_for_include_deleted_false_data = TestData(
    data_in={"include_deleted": False},
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?include_deleted=false&token=TESTTOKEN"
    ]
)

get_time_for_proj_and_activity_data = TestData(
    data_in={
        "project": ["gwm"],
        "activity": ["dev"]
    },
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?activity=dev&project=gwm&token=TESTTOKEN"
    ]
)

get_time_for_activity_x3_data = TestData(
    data_in={
        "activity": ["dev", "rev", "hd"]
    },
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times?activity=dev&activity=rev&activity=hd&token=TESTTOKEN"
    ]
)

get_time_with_uuid_data = TestData(
    data_in={
        "uuid": str(test_uuid)
    },
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times/{}?token=TESTTOKEN".format(test_uuid)
    ]
)

get_time_with_uuid_and_activity_data = TestData(
    data_in={
        "uuid": test_uuid,
        "activity": ["dev"]
    },
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times/{}?token=TESTTOKEN".format(test_uuid)
    ]
)

get_time_with_uuid_and_include_revisions_data = TestData(
    data_in={
        "uuid": test_uuid,
        "include_revisions": True
    },
    data_out=[
        {"this": "should be in a list"},
        "http://ts.example.com/v1/times/{}?include_revisions=true&token=TESTTOKEN".format(test_uuid)
    ]
)
