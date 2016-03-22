import pymesync
import unittest
import datetime


class TestMockPymesync(unittest.TestCase):

    def setUp(self):
        baseurl = "http://ts.example.com/v1"
        self.ts = pymesync.TimeSync(baseurl, test=True)
        self.ts.authenticate("testuser", "testpassword", "password")

    def tearDown(self):
        del(self.ts)

    def test_mock_authenticate(self):
        self.ts.token = None
        self.assertEquals(self.ts.authenticate("example", "ex", "password"),
                          {"token": "TESTTOKEN"})
        self.assertEquals(self.ts.token, "TESTTOKEN")

    def test_mock_token_expiration_time(self):
        self.assertEquals(self.ts.token_expiration_time(),
                          datetime.datetime(2016, 1, 13, 11, 45, 34))

    def test_mock_create_time(self):
        parameter_dict = {
            "duration": 12,
            "user": "example-2",
            "project": "ganeti_web_manager",
            "activities": ["docs"],
            "notes": "Worked on documentation toward settings configuration.",
            "issue_uri": "https://github.com/osuosl/ganeti_webmgr/issues",
            "date_worked": "2014-04-17"
        }

        expected_result = {
            "duration": 12,
            "user": "example-2",
            "project": "ganeti_web_manager",
            "activities": ["docs"],
            "notes": "Worked on documentation toward settings configuration.",
            "issue_uri": "https://github.com/osuosl/ganeti_webmgr/issues",
            "date_worked": "2014-04-17",
            "created_at": "2015-05-23",
            "updated_at": None,
            "deleted_at": None,
            "uuid": "838853e3-3635-4076-a26f-7efr4e60981f",
            "revision": 1
        }
        self.assertEquals(self.ts.create_time(parameter_dict), expected_result)

    def test_mock_update_time(self):
        parameter_dict = {
            "duration": 19,
            "user": "red-leader",
            "activities": ["hello", "world"],
        }
        updated_param = {
            "duration": 19,
            "user": "red-leader",
            "activities": ["hello", "world"],
            "project": ["ganeti"],
            "notes": None,
            "issue_uri": "https://github.com/osuosl/ganeti_webmgr/issues/56",
            "date_worked": "2015-08-07",
            "created_at": "2014-06-12",
            "updated_at": "2015-10-18",
            "deleted_at": None,
            "uuid": "fake-uuid",
            "revision": 2
        }
        self.assertEquals(self.ts.update_time(parameter_dict, "fake-uuid"),
                          updated_param)

    def test_mock_create_time_with_string_duration(self):
        parameter_dict = {
            "duration": "3h30m",
            "user": "example-2",
            "project": "ganeti_web_manager",
            "activities": ["docs"],
            "notes": "Worked on documentation toward settings configuration.",
            "issue_uri": "https://github.com/osuosl/ganeti_webmgr/issues",
            "date_worked": "2014-04-17"
        }

        expected_result = {
            "duration": 12600,
            "user": "example-2",
            "project": "ganeti_web_manager",
            "activities": ["docs"],
            "notes": "Worked on documentation toward settings configuration.",
            "issue_uri": "https://github.com/osuosl/ganeti_webmgr/issues",
            "date_worked": "2014-04-17",
            "created_at": "2015-05-23",
            "updated_at": None,
            "deleted_at": None,
            "uuid": "838853e3-3635-4076-a26f-7efr4e60981f",
            "revision": 1
        }
        self.assertEquals(self.ts.create_time(parameter_dict), expected_result)

    def test_mock_update_time_with_string_duration(self):
        parameter_dict = {
            "duration": "3h35m",
            "user": "red-leader",
            "activities": ["hello", "world"],
        }
        updated_param = {
            "duration": 12900,
            "user": "red-leader",
            "activities": ["hello", "world"],
            "project": ["ganeti"],
            "notes": None,
            "issue_uri": "https://github.com/osuosl/ganeti_webmgr/issues/56",
            "date_worked": "2015-08-07",
            "created_at": "2014-06-12",
            "updated_at": "2015-10-18",
            "deleted_at": None,
            "uuid": "fake-uuid",
            "revision": 2
        }
        self.assertEquals(self.ts.update_time(parameter_dict, "fake-uuid"),
                          updated_param)

    def test_mock_create_project(self):
        parameter_dict = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "users": {
                "mrsj": {"member": True, "spectator": True, "manager": True},
                "thai": {"member": True, "spectator": False, "manager": False}
            }
        }

        expected_result = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "TimeSync API",
            "slugs": ["timesync", "time"],
            "uuid": "309eae69-21dc-4538-9fdc-e6892a9c4dd4",
            "created_at": "2015-05-23",
            "updated_at": None,
            "deleted_at": None,
            "revision": 1,
            "users": {
                "mrsj": {"member": True, "spectator": True, "manager": True},
                "thai": {"member": True, "spectator": False, "manager": False}
            }
        }

        self.assertEquals(self.ts.create_project(parameter_dict),
                          expected_result)

    def test_mock_update_project(self):
        parameter_dict = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "pymesync",
        }

        expected_result = {
            "uri": "https://code.osuosl.org/projects/timesync",
            "name": "pymesync",
            "slugs": ["ps"],
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

        self.assertEquals(self.ts.update_project(parameter_dict, "ps"),
                          expected_result)

    def test_mock_create_activity(self):
        parameter_dict = {
            "name": "Quality Assurance/Testing",
            "slug": "qa"
        }

        expected_result = {
            "name": "Quality Assurance/Testing",
            "slug": "qa",
            "uuid": "cfa07a4f-d446-4078-8d73-2f77560c35c0",
            "created_at": "2013-07-27",
            "updated_at": None,
            "deleted_at": None,
            "revision": 1
        }

        self.assertEquals(self.ts.create_activity(parameter_dict),
                          expected_result)

    def test_mock_update_activity(self):
        parameter_dict = {"name": "Code in the wild"}

        expected_result = {
            "name": "Code in the wild",
            "slug": "ciw",
            "uuid": "3cf78d25-411c-4d1f-80c8-a09e5e12cae3",
            "created_at": "2014-04-16",
            "updated_at": "2014-04-17",
            "deleted_at": None,
            "revision": 2
        }

        self.assertEquals(self.ts.update_activity(parameter_dict, "ciw"),
                          expected_result)

    def test_mock_create_user(self):
        parameter_dict = {
            "username": "example",
            "password": "password",
            "display_name": "X. Ample User",
            "email": "example@example.com"
        }

        expected_result = {
            "username": "example",
            "display_name": "X. Ample User",
            "email": "example@example.com",
            "active": True,
            "site_admin": False,
            "site_manager": False,
            "site_spectator": False,
            "created_at": "2015-05-23",
            "deleted_at": None
        }

        self.assertEquals(self.ts.create_user(parameter_dict), expected_result)

    def test_mock_update_user(self):
        parameter_dict = {
            "username": "red-leader",
            "email": "red-leader@yavin.com",
            "site_spectator": True
        }

        expected_result = {
            "username": "red-leader",
            "display_name": "Mr. Example",
            "email": "red-leader@yavin.com",
            "active": True,
            "site_admin": False,
            "site_manager": False,
            "site_spectator": True,
            "created_at": "2015-02-29",
            "deleted_at": None
        }

        self.assertEquals(self.ts.update_user(parameter_dict, "example"),
                          expected_result)

    def test_mock_get_times_with_uuid(self):
        expected_result = [{
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
            "uuid": "example-uuid"
        }]

        self.assertEquals(self.ts.get_times({"uuid": "example-uuid"}),
                          expected_result)

    def test_mock_get_times_no_uuid(self):
        expected_result = [
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
                "uuid": "c3706e79-1c9a-4765-8d7f-89b4544cad56"
            },
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
            },
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
        ]

        self.assertEquals(self.ts.get_times(), expected_result)

    def test_mock_get_projects_with_slug(self):
        expected_result = [{
            "uri": "https://code.osuosl.org/projects/ganeti-webmgr",
            "name": "Ganeti Web Manager",
            "slugs": ["ganeti"],
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
        }]

        self.assertEquals(self.ts.get_projects({"slug": "ganeti"}),
                          expected_result)

    def test_mock_get_projects_no_slug(self):
        expected_result = [
            {
                "uri": "https://code.osuosl.org/projects/ganeti-webmgr",
                "name": "Ganeti Web Manager",
                "slugs": ["gwm"],
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
            },
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
            },
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
        ]

        self.assertEquals(self.ts.get_projects(), expected_result)

    def test_mock_get_activities_with_slug(self):
        expected_result = [{
            "name": "Documentation",
            "slugs": ["docudocs"],
            "uuid": "adf036f5-3d49-4a84-bef9-062b46380bbf",
            "revision": 5,
            "created_at": "2014-04-17",
            "deleted_at": None,
            "updated_at": None
        }]

        self.assertEquals(self.ts.get_activities({"slug": "docudocs"}),
                          expected_result)

    def test_mock_get_activities_no_slug(self):
        expected_result = [
            {
                "name": "Documentation",
                "slugs": ["docs"],
                "uuid": "adf036f5-3d49-4a84-bef9-062b46380bbf",
                "revision": 5,
                "created_at": "2014-04-17",
                "deleted_at": None,
                "updated_at": None
            },
            {
                "name": "Coding",
                "slugs": ["code", "dev"],
                "uuid": "adf036f5-3d49-bbbb-rrrr-062b46380bbf",
                "revision": 1,
                "created_at": "2014-04-17",
                "deleted_at": None,
                "updated_at": None
            },
            {
                "name": "Planning",
                "slugs": ["plan", "prep"],
                "uuid": "adf036f5-3d49-cccc-ssss-062b46380bbf",
                "revision": 1,
                "created_at": "2014-04-17",
                "deleted_at": None,
                "updated_at": None
            }
        ]

        self.assertEquals(self.ts.get_activities(), expected_result)

    def test_mock_get_users_with_username(self):
        expected_result = [{
            "username": "example-user",
            "display_name": "X. Ample User",
            "email": "example@example.com",
            "active": True,
            "site_admin": False,
            "site_manager": False,
            "site_spectator": False,
            "created_at": "2015-02-29",
            "deleted_at": None
        }]

        self.assertEquals(self.ts.get_users("example-user"), expected_result)

    def test_mock_get_users_no_username(self):
        expected_result = [
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

        self.assertEquals(self.ts.get_users(), expected_result)

    def test_mock_delete_object(self):
        self.assertEquals(self.ts.delete_time("junk"), [{"status": 200}])
        self.assertEquals(self.ts.delete_project("junk"), [{"status": 200}])
        self.assertEquals(self.ts.delete_activity("junk"), [{"status": 200}])
        self.assertEquals(self.ts.delete_user("junk"), [{"status": 200}])

    def test_mock_project_users(self):
        expected_result = {
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

        self.assertEquals(self.ts.project_users(project="ff"), expected_result)

    def test_mock_project_users_no_slug(self):
        expected_result = {self.ts.error: "Missing project slug, please "
                                          "include in method call"}
        self.assertEquals(self.ts.project_users(), expected_result)


if __name__ == "__main__":
    unittest.main()
