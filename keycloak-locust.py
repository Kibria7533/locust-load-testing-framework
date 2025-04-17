from locust import HttpUser, task, between

class KeycloakUser(HttpUser):
    wait_time = between(0.01, 0.05)

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post(
            "/realms/master/protocol/openid-connect/token",
            data={
                "client_id": "admin-cli",
                "username": "admin",
                "password": "qazwsx@321",
                "grant_type": "password"
            }
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            self.client.headers.update({"Authorization": f"Bearer {token}"})
        else:
            print("Login failed:", response.status_code, response.text)

    @task
    def get_token_loop(self):
        # This will be executed repeatedly after login
        self.login()
