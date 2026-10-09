import re


class UserTests:
    """Helpers for User tests."""

    def generate_creds(self, unique_name: str):
        """Return an object containing a unique email and password."""
        return {
            "email": f"{unique_name}@test.com",
            "password": "12345"
        }


class TestRegisterEndpoint(UserTests):
    """Tests for the /register endpoint"""

    def test_user_register_valid(self, client):
        """Verify success status when a new user is created"""

        credentials = self.generate_creds("user_register_valid")
        response = client.post("/register", json=credentials)

        assert response.status_code == 201
        assert response.json["message"]

    def test_conflicting_user_registration(self, client):
        """Verify rejection when user already exsists on sign-in."""

        credentials = self.generate_creds("conflicting_user_registration")
        client.post("/register", json=credentials)
        response = client.post("/register", json=credentials)

        assert "access_token" not in response.json
        assert "refresh_token" not in response.json
        assert response.status_code == 409


class TestSignInEndpoint(UserTests):
    """Tests for the /signin endpoint"""

    def _is_jwt_format(self, candidate):
        """Confirm candidate is formatted as a JWT. Does not validate."""
        jwt_regex = r"^[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+"
        return re.match(jwt_regex, candidate)

    def test_valid_access_token_response(self, client):
        """Verify valid access token returned on successful sign-in."""

        credentials = self.generate_creds("valid_access_token_response")
        client.post("/register", json=credentials)
        response = client.post("/signin", json=credentials)

        assert self._is_jwt_format(response.json["access_token"])
        assert response.status_code == 200

    def test_valid_refresh_token_response(self, client):
        """Verify valid refresh token returned on successful sign-in."""

        credentials = self.generate_creds("valid_refresh_token_response")
        client.post("/register", json=credentials)
        response = client.post("/signin", json=credentials)

        assert self._is_jwt_format(response.json["refresh_token"])
        assert response.status_code == 200


class TestSignOutEndpoint(UserTests):
    """Tests for the /signout endpoint"""

    def test_valid_sign_out_response(self, client):
        """Verify signout with valid JWT."""

        # create user
        credentials = self.generate_creds("valid_sign_out_response")
        client.post("/register", json=credentials)

        # sign in
        sign_in_response = client.post("/signin", json=credentials)
        access_token = sign_in_response.json["access_token"]

        # sign out
        header_obj = {"Authorization": f"Bearer {access_token}"}
        sign_out_response = client.post("/signout", headers=header_obj)

        assert sign_out_response.json["message"]
        assert sign_out_response.json["success"]
        assert sign_out_response.status_code == 200

    def test_double_sign_out_response(self, client):
        """Verify signout response code when already signed out."""

        # create user
        credentials = self.generate_creds("double_sign_out_response")
        client.post("/register", json=credentials)

        # sign in
        sign_in_response = client.post("/signin", json=credentials)
        access_token = sign_in_response.json["access_token"]

        # initial sign out
        header_obj = {"Authorization": f"Bearer {access_token}"}
        client.post("/signout", headers=header_obj)

        # attenot to sign out a second time
        sign_out_response = client.post("/signout", headers=header_obj)

        assert sign_out_response.status_code == 401
