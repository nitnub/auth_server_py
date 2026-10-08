import re


class TestRegisterEndpoint:
    """Tests for the /register endpoint"""

    def test_verify_test2(self, client):
        """Verify test endpoint is working"""

        response = client.post("/test2")
        assert response.json["val"] == "moo"

    def test_user_register_valid(self, client):
        """Verify success status when a new user is created"""

        response = client.post("/register", json={
            "email": "joe@mysite.com",
            "password": "12345"
        })
        assert response.status_code == 201
        assert response.json["message"]


class TestSignInEndpoint:
    """Tests for the /signin endpoint"""

    jwt_regex = r"^[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+"

    def test_valid_access_token_response(self, client):
        """Verify valid access token returned on successful sign-in."""

        user_creds = {
            "email": "joe@test_valid_access_token_response.com",
            "password": "12345"
        }
        client.post("/register", json=user_creds)
        response = client.post("/signin", json=user_creds)
        assert re.match(self.jwt_regex, response.json["access_token"])
        assert response.status_code == 200

    def test_valid_refresh_token_response(self, client):
        """Verify valid refresh token returned on successful sign-in."""

        user_creds = {
            "email": "joe@test_valid_refresh_token_response.com",
            "password": "12345"
        }
        client.post("/register", json=user_creds)
        response = client.post("/signin", json=user_creds)
        assert re.match(self.jwt_regex, response.json["refresh_token"])
        assert response.status_code == 200
