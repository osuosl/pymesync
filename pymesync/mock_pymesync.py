import datetime

def authenticate():
    return {"token": "TESTTOKEN"}


def token_expiration_time():
    return datetime.datetime(2016, 1, 13, 11, 45, 34)


def create_time(p_dict):
    """Sends time to baseurl (TimeSync)"""
    p_dict["created_at"] = "2015-05-23"
    p_dict["updated_at"] = None
    p_dict["deleted_at"] = None
    p_dict["uuid"] = "838853e3-3635-4076-a26f-7efr4e60981f"
    p_dict["revision"] = 1
    p_dict["notes"] = p_dict["notes"] if p_dict["notes"] else None
    p_dict["issue_uri"] = p_dict["issue_uri"] if p_dict["issue_uri"] else None
    return p_dict


def update_time(p_dict, uuid):
    """Updates time by uuid"""
    updated_param = {
        "duration": p_dict["duration"] if "duration" in p_dict else 18,
        "user": p_dict["user"] if "user" in p_dict else "example-user",
        "activities": p_dict["activities"] if "activities" in p_dict else (
            ["qa"]),
        "project": p_dict["project"] if "project" in p_dict else ["ganeti"],
        "notes": p_dict["notes"] if "notes" in p_dict else None,
        "issue_uri": p_dict["issue_uri"] if "issue_uri" in p_dict else (
            "https://github.com/osuosl/ganeti_webmgr/issues/56"),
        "date_worked": p_dict["date_worked"] if "date_worked" in p_dict else (
            "2015-08-07"),
        "created_at": "2014-06-12",
        "updated_at": "2015-10-18",
        "deleted_at": None,
        "uuid": uuid,
        "revision": 2
    }
    return updated_param


def create_project(p_dict):
    """Creates project"""
    p_dict["users"] = {
        "mrsj": {"member": True, "spectator": True, "manager": True},
        "tschuy": {"member": True, "spectator": False, "manager": False}
    } if "users" not in p_dict else p_dict["users"]
    p_dict["uuid"] = "309eae69-21dc-4538-9fdc-e6892a9c4dd4"
    p_dict["revision"] = 1
    p_dict["created_at"] = "2015-05-23"
    p_dict["updated_at"] = None
    p_dict["deleted_at"] = None
    p_dict["uri"] = p_dict["uri"] if "uri" in p_dict else None
    return p_dict


def update_project(p_dict, slug):
    """Updates project by slug"""
    updated_param = {
        "uri": p_dict["uri"] if "uri" in p_dict else None,
        "name": p_dict["name"] if "name" in p_dict else "TimeSync API",
        "slugs": p_dict["slugs"] if "slugs" in p_dict else [slug],
        "created_at": "2014-04-16",
        "updated_at": "2014-04-18",
        "deleted_at": None,
        "uuid": "309eae69-21dc-4538-9fdc-e6892a9c4dd4",
        "revision": 2,
        "users": {
            "members": [
                "patcht",
                "tschuy"
            ],
            "spectators": [
                "tschuy"
            ],
            "managers": [
                "tschuy"
            ]
        }
    }
    return updated_param


def create_activity(p_dict):
    """Creates activity"""
    p_dict["uuid"] = "cfa07a4f-d446-4078-8d73-2f77560c35c0"
    p_dict["created_at"] = "2013-07-27"
    p_dict["updated_at"] = None
    p_dict["deleted_at"] = None
    p_dict["revision"] = 1
    return p_dict


def update_activity(p_dict, slug):
    """Updates activity by slug"""
    updated_param = {
        "name": p_dict["name"] if "name" in p_dict else "Testing Infra",
        "slug": p_dict["slug"] if "slug" in p_dict else slug,
        "uuid": "3cf78d25-411c-4d1f-80c8-a09e5e12cae3",
        "created_at": "2014-04-16",
        "updated_at": "2014-04-17",
        "deleted_at": None,
        "revision": 2
    }
    return updated_param


def create_user(p_dict):
    """Creates a user"""
    p_dict["active"] = True
    p_dict["site_admin"] = False if "site_admin" not in p_dict else (
            p_dict["site_admin"])
    p_dict["site_manager"] = False if "site_manager" not in p_dict else (
            p_dict["site_manager"])
    p_dict["site_spectator"] = False if "site_spectator" not in p_dict else (
            p_dict["site_spectator"])
    p_dict["created_at"] = "2015-05-23"
    p_dict["deleted_at"] = None
    del(p_dict["password"])
    return p_dict


def update_user(p_dict, username):
    """Updates user by username"""
    updated_param = {
        "username": p_dict["username"] if "username" in p_dict else username,
        "display_name": p_dict["display_name"] if "display_name" in p_dict else (
            "Mr. Example"),
        "email": p_dict["email"] if "email" in p_dict else (
            "examplej@example.com"),
        "active": True,
        "site_admin": False if "site_admin" not in p_dict else (
            p_dict["site_admin"]),
        "site_manager": False if "site_manager" not in p_dict else (
            p_dict["site_manager"]),
        "site_spectator": False if "site_spectator" not in p_dict else (
            p_dict["site_spectator"]),
        "created_at": "2015-02-29",
        "deleted_at": None
    }
    return updated_param


def get_times(uuid):
    """Get times from TimeSync"""
    p_list = [
        {
            "duration": 12,
            "user": "userone",
            "project": ["ganeti-webmgr", "gwm"],
            "activities": ["docs", "planning"],
            "notes": "Worked on documentation.",
            "issue_uri": "https://github.com/osuosl/ganeti_webmgr",
            "date_worked": "2014-04-17",
            "revision": 1,
            "created_at": "2014-04-17",
            "updated_at": None,
            "deleted_at": None,
            "uuid": uuid if uuid else "c3706e79-1c9a-4765-8d7f-89b4544cad56"
        }
    ]
    if not uuid:
        p_list.append(
            {
                "duration": 13,
                "user": "usertwo",
                "project": ["ganeti-webmgr", "gwm"],
                "activities": ["code", "planning"],
                "notes": "Worked on coding",
                "issue_uri": "https://github.com/osuosl/ganeti_webmgr",
                "date_worked": "2014-04-17",
                "revision": 1,
                "created_at": "2014-04-17",
                "updated_at": None,
                "deleted_at": None,
                "uuid": "12345676-1c9a-rrrr-bbbb-89b4544cad56"
            }
        )

        p_list.append(
            {
                "duration": 14,
                "user": "userthree",
                "project": ["timesync", "ts"],
                "activities": ["code"],
                "notes": "Worked on coding",
                "issue_uri": "https://github.com/osuosl/timesync",
                "date_worked": "2014-04-17",
                "revision": 1,
                "created_at": "2014-04-17",
                "updated_at": None,
                "deleted_at": None,
                "uuid": "12345676-1c9a-ssss-cccc-89b4544cad56"
            }
        )
    return p_list


def get_projects(slug):
    """Get project information from TimeSync"""
    p_list = [
        {
            "uri": "https://code.osuosl.org/projects/ganeti-webmgr",
            "name": "Ganeti Web Manager",
            "slugs": [slug if slug else "gwm"],
            "uuid": "a034806c-00db-4fe1-8de8-514575f31bfb",
            "revision": 4,
            "created_at": "2014-07-17",
            "deleted_at": None,
            "updated_at": "2014-07-20",
            "users": {
                "members": [
                    "patcht",
                    "tschuy"
                ],
                "spectators": [
                    "tschuy"
                ],
                "managers": [
                    "tschuy"
                ]
            }
        }
    ]
    if not slug:
        p_list.append(
            {
                "uri": "https://code.osuosl.org/projects/timesync",
                "name": "TimeSync",
                "slugs": ["timesync", "ts"],
                "uuid": "a034806c-rrrr-bbbb-8de8-514575f31bfb",
                "revision": 2,
                "created_at": "2014-07-17",
                "deleted_at": None,
                "updated_at": "2014-07-20",
                "users": {
                    "members": [
                        "patcht",
                        "tschuy",
                        "mrsj"
                    ],
                    "spectators": [
                        "tschuy",
                        "mrsj"
                    ],
                    "managers": [
                        "tschuy"
                    ]
                }
            }
        )

        p_list.append(
            {
                "uri": "https://code.osuosl.org/projects/pymesync",
                "name": "pymesync",
                "slugs": ["pymesync", "ps"],
                "uuid": "a034806c-ssss-cccc-8de8-514575f31bfb",
                "revision": 1,
                "created_at": "2014-07-17",
                "deleted_at": None,
                "updated_at": "2014-07-20",
                "users": {
                    "members": [
                        "patcht",
                        "tschuy",
                        "mrsj",
                        "MaraJade",
                        "thai"
                    ],
                    "spectators": [
                        "tschuy",
                        "mrsj"
                    ],
                    "managers": [
                        "mrsj"
                    ]
                }
            }
        )
    return p_list


def get_activities(slug):
    """Get activity information from TimeSync"""
    p_list = [
        {
            "name": "Documentation",
            "slugs": [slug if slug else "docs"],
            "uuid": "adf036f5-3d49-4a84-bef9-062b46380bbf",
            "revision": 5,
            "created_at": "2014-04-17",
            "deleted_at": None,
            "updated_at": None
        }
    ]
    if not slug:
        p_list.append(
            {
                "name": "Coding",
                "slugs": ["code", "dev"],
                "uuid": "adf036f5-3d49-bbbb-rrrr-062b46380bbf",
                "revision": 1,
                "created_at": "2014-04-17",
                "deleted_at": None,
                "updated_at": None
            }
        )

        p_list.append(
            {
                "name": "Planning",
                "slugs": ["plan", "prep"],
                "uuid": "adf036f5-3d49-cccc-ssss-062b46380bbf",
                "revision": 1,
                "created_at": "2014-04-17",
                "deleted_at": None,
                "updated_at": None
            }
        )
    return p_list


def get_users(username):
    """Get user information from TimeSync"""
    if username:
        p_dict = [{
            "username": username,
            "display_name": "X. Ample User",
            "email": "example@example.com",
            "active": True,
            "site_admin": False,
            "site_spectator": False,
            "site_manager": False,
            "created_at": "2015-02-29",
            "deleted_at": None
        }]
    else:
        p_dict = [
            {
                "username": "userone",
                "display_name": "One Is The Loneliest Number",
                "email": "exampleone@example.com",
                "active": True,
                "site_admin": False,
                "site_manager": False,
                "site_spectator": False,
                "created_at": "2015-02-29",
                "deleted_at": None
            },
            {
                "username": "usertwo",
                "display_name": "Two Can Be As Bad As One",
                "email": "exampletwo@example.com",
                "active": True,
                "site_admin": False,
                "site_manager": False,
                "site_spectator": False,    
                "created_at": "2015-02-29",
                "deleted_at": None
            },
            {
                "username": "userthree",
                "display_name": "Yes It's The Saddest Experience",
                "email": "examplethree@example.com",
                "active": True,
                "site_admin": False,
                "site_manager": False,
                "site_spectator": False,    
                "created_at": "2015-02-29",
                "deleted_at": None
            },
            {
                "username": "userfour",
                "display_name": "You'll Ever Do",
                "email": "examplefour@example.com",
                "active": True,
                "site_admin": False,
                "site_manager": False,
                "site_spectator": False,    
                "created_at": "2015-02-29",
                "deleted_at": None
            }
        ]
    return p_dict


def delete_object():
    """Delete an object from TimeSync"""
    return [{"status": 200}]


def project_users():
    """Return list of users and permissions from TimeSync"""
    users = {
        u'malcolm': [u'member', u'manager'],
        u'jayne':   [u'member'],
        u'kaylee':  [u'member'],
        u'zoe':     [u'member'],
        u'hoban':   [u'member'],
        u'simon':   [u'spectator'],
        u'river':   [u'spectator'],
        u'derrial': [u'spectator'],
        u'inara':   [u'spectator']
    }

    return users
