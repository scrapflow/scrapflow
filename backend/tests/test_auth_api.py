import pytest
from fastapi import status


class TestAuthLoginEndpoint:
    """HTTP-level unit tests for the /api/v1/auth/login endpoint."""

    LOGIN_URL = "/api/v1/auth/login"

    def test_login_success_with_username(self, client, mock_db_session, active_user, plain_password):
        """User can log in successfully with valid username and password."""
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = active_user

        response = client.post(
            self.LOGIN_URL,
            json={"username": active_user.username, "password": plain_password},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Login successful!"
        assert data["username"] == active_user.username
        assert data["email"] == active_user.email

    def test_login_success_with_email(self, client, mock_db_session, active_user, plain_password):
        """User can log in successfully with valid email and password."""
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = active_user

        response = client.post(
            self.LOGIN_URL,
            json={"username": active_user.email, "password": plain_password},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Login successful!"
        assert data["username"] == active_user.username
        assert data["email"] == active_user.email

    def test_login_user_not_found(self, client, mock_db_session):
        """Returns 401 Unauthorized when the username or email is not found."""
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = None

        response = client.post(
            self.LOGIN_URL,
            json={"username": "nonexistent_user", "password": "some_password"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Incorrect username or password."
        assert response.headers.get("WWW-Authenticate") == "Bearer"

    def test_login_incorrect_password(self, client, mock_db_session, active_user):
        """Returns 401 Unauthorized when the password is wrong."""
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = active_user

        response = client.post(
            self.LOGIN_URL,
            json={"username": active_user.username, "password": "wrong_password_123"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Incorrect username or password."
        assert response.headers.get("WWW-Authenticate") == "Bearer"

    def test_login_inactive_user(self, client, mock_db_session, inactive_user, plain_password):
        """Returns 400 Bad Request when the user account is inactive."""
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = inactive_user

        response = client.post(
            self.LOGIN_URL,
            json={"username": inactive_user.username, "password": plain_password},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Inactive account."

    def test_login_missing_username(self, client):
        """Returns 422 Unprocessable Entity when username is missing."""
        response = client.post(
            self.LOGIN_URL,
            json={"password": "anypassword"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_login_missing_password(self, client):
        """Returns 422 Unprocessable Entity when password is missing."""
        response = client.post(
            self.LOGIN_URL,
            json={"username": "testuser"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_login_empty_body(self, client):
        """Returns 422 Unprocessable Entity when request body is empty JSON."""
        response = client.post(
            self.LOGIN_URL,
            json={},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
