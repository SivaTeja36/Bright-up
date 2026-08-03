from .test_base import TestBase


class TestLogin(TestBase):
    def test_superadmin_logins_successfully(self):
        login_result = self.client.post(
            "/login", json=self.superadmin_user_credentials
        )
        assert login_result.status_code == 200
        assert login_result.json()["data"]["token"]

    def test_invalid_user_cant_login(self):
        login_result = self.client.post(
            "/login", json=self.invalid_user_credentials
        )
        assert login_result.status_code == 400
