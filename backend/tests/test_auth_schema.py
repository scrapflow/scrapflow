import pytest
from pydantic import ValidationError
from app.api.v1.endpoints.auth import LoginRequest


class TestLoginRequestSchema:
    def test_valid_login_request(self):
        """Test valid initialization of LoginRequest with username and password."""
        payload = {"username": "testuser", "password": "securepassword"}
        request = LoginRequest(**payload)

        assert request.username == "testuser"
        assert request.password == "securepassword"

    def test_missing_username_raises_validation_error(self):
        """Test that omitting username raises Pydantic ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            LoginRequest(password="securepassword")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("username",) for e in errors)

    def test_missing_password_raises_validation_error(self):
        """Test that omitting password raises Pydantic ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            LoginRequest(username="testuser")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("password",) for e in errors)

    def test_empty_payload_raises_validation_error(self):
        """Test that an empty payload raises ValidationError with two missing field errors."""
        with pytest.raises(ValidationError) as exc_info:
            LoginRequest()

        errors = exc_info.value.errors()
        missing_fields = {e["loc"][0] for e in errors}
        assert "username" in missing_fields
        assert "password" in missing_fields
