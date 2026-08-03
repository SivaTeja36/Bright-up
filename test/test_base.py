from fastapi.testclient import TestClient

from app.main import app


class TestBase:
    client: TestClient

    superadmin_user_credentials = {
        "email": "vantasivateja@gmail.com",
        "password": "String@123",
    }

    invalid_user_credentials = {
        "email": "invalid@unittest.com",
        "password": "invalidPass",
    }

    def setup_method(self):
        self.client = TestClient(app)

    def login_as_super_admin(self):
        login_result = self.client.post(
            "/login", json=self.superadmin_user_credentials
        )
        login_result.raise_for_status()
        return login_result.json()["data"]["token"]

    def get_authenticated_client(self):
        token = self.login_as_super_admin()
        self.client.headers.clear()
        self.client.headers.update({"Authorization": f"Bearer {token}"})
        return self.client
