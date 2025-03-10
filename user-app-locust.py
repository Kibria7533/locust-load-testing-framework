from locust import HttpUser, task, between
import gevent



class InElectionApp(HttpUser):
    wait_time = between(1, 3)  # Simulates user wait time between requests

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.verify = False  # Disable SSL verification (for testing only)

    @task
    def entry_page(self):
        """Synchronous: Simulate user visiting the Entry Page (requests executed one after another)"""
        self.client.get("/ec-user-app/api/v2/private/notifications", name="Entry Page - Notifications")
        self.client.get("/ec-user-app/api/v2/private/elections", name="Entry Page - Elections")
        self.client.get("/ec-user-app/api/v2/private/election-types", name="Entry Page - Election Types")
        self.client.get("/ec-user-app/api/v2/private/candidate-types", name="Entry Page - Candidate Types")

    @task
    def user_mock_info(self):
        payload = {
            "dob": "1993-11-25",
            "search_value": "1234567891"
        }
        headers = {
            "Content-Type": "application/json"
        }

        self.client.post(
            "/ec-user-app/api/v2/private/mock-user-voter-area?election_schedule_id=1",
            json=payload,
            headers=headers,
            name="User Info"
        )

    @task
    def constituency_info(self):
        """Asynchronous: Requests for Constituency Info run in parallel"""
        gevent.joinall([
            gevent.spawn(self.client.get, "/ec-user-app/api/v2/private/districts?election_schedule_id=14",
                         name="Constituency Info"),
            gevent.spawn(self.client.get,
                         "/ec-presiding-officer-service/api/v2/private/election/14/constituency-time-wise-vote-count/2",
                         name="Constituency Vote Count"),
            gevent.spawn(self.client.get,
                         "/ec-user-result-management-service/api/v2/private/candidates/election/20/settings/865",
                         name="Constituency Candidates"),
            gevent.spawn(self.client.get, "/ec-user-result-management-service/api/v2/private/election/20/centers/868",
                         name="Election Wise Constituency Centers")
        ])
        gevent.joinall([
            gevent.spawn(self.client.get, "/ec-user-result-management-service/api/v2/private/center/43544",
                         name="Constituency Center"),
            gevent.spawn(self.client.get,
                         "/ec-presiding-officer-service/api/v2/private/election/14/center-time-wise-vote-count/43449",
                         name="Constituency Center Vote Count")
        ])

    @task
    def election_page(self):
        """Asynchronous: Requests for Election Page run in parallel"""
        gevent.joinall([
            gevent.spawn(self.client.get, "/ec-user-app/api/v2/private/districts?election_schedule_id=14",
                         name="Election Page - Districts"),
            gevent.spawn(self.client.get,
                         "/ec-user-result-management-service/api/v2/private/settings-winner/election/1",
                         name="Election Page - Winner Settings")
        ])

    @task
    def election_setting_detail_page(self):
        """Asynchronous: Requests for Election Setting Detail Page run in parallel"""
        gevent.joinall([
            gevent.spawn(self.client.get, "/ec-user-app/api/v2/private/election-metadata/14",
                         name="Election Setting Detail - Metadata"),
            gevent.spawn(self.client.get, "/ec-user-app/api/v2/private/notices?election_schedule_id=14",
                         name="Election Setting Detail - Notices"),
            gevent.spawn(self.client.get, "/ec-user-app/api/v2/private/election-laws?election_schedule_id=14",
                         name="Election Setting Detail - Laws"),
            gevent.spawn(self.client.get, "/ec-user-app/api/v2/private/political-parties?election_schedule_id=14",
                         name="Election Setting Detail - Political Parties")
        ])

    @task
    def day_and_after_election_page(self):
        """Asynchronous: Requests for Day & After Election Page run in parallel"""
        gevent.joinall([
            gevent.spawn(self.client.get, "/ec-user-result-management-service/api/v2/private/election/14/centers/6",
                         name="Election Centers"),
            gevent.spawn(self.client.get,
                         "/ec-user-result-management-service/api/v2/private/settings-result/election/14/settings/6",
                         name="Election Vote Count"),
            gevent.spawn(self.client.get,
                         "/ec-user-result-management-service/api/v2/private/center-result/election/14/voting-center?polling_center_id=43449",
                         name="Specific Voting Center Vote Count"),
            gevent.spawn(self.client.get,
                         "/ec-user-result-management-service/api/v2/private/result/election/14/settings/6",
                         name="Election Voter Count")
        ])
