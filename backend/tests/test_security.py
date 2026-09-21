import pytest
from app.core.security import get_password_hash, verify_password


class TestSecurityUtils:
    def test_get_password_hash_creates_valid_hash(self):
        """Test that get_password_hash returns a non-empty bcrypt hash string."""
        password = "mysecretpassword123"
        hashed = get_password_hash(password)

        assert isinstance(hashed, str)
        assert hashed != password
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    def test_get_password_hash_generates_unique_salt(self):
        """Test that hashing the same password twice yields different hashes due to salt."""
        password = "mysecretpassword123"
        hash_1 = get_password_hash(password)
        hash_2 = get_password_hash(password)

        assert hash_1 != hash_2
        # Both hashes should still verify correctly with the original password
        assert verify_password(password, hash_1) is True
        assert verify_password(password, hash_2) is True

    def test_verify_password_success(self):
        """Test that verify_password returns True for the matching plain password."""
        password = "correct_horse_battery_staple"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect_password(self):
        """Test that verify_password returns False for an incorrect plain password."""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_invalid_hash(self):
        """Test that verify_password handles invalid/corrupted hash without raising exceptions."""
        assert verify_password("some_password", "invalid_hash_string") is False
        assert verify_password("some_password", "") is False

    def test_verify_password_empty_password(self):
        """Test that an empty plain password fails verification against a valid hash."""
        hashed = get_password_hash("non_empty_password")
        assert verify_password("", hashed) is False
