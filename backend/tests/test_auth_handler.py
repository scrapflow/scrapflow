import pytest
from fastapi import HTTPException, status
from app.api.v1.endpoints.auth import login, LoginRequest


@pytest.mark.anyio
class TestAuthLoginHandler:
    """Direct unit tests for the async login(...) endpoint function."""

    async def test_login_handler_success_with_username(
        self, mock_db_session, active_user, plain_password
    ):
        """Handler returns success dict when valid username and password match."""
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = active_user
        login_data = LoginRequest(username=active_user.username, password=plain_password)

        result = await login(login_data=login_data, db=mock_db_session)

        mock_db_session.execute.assert_called_once()
        assert result == {
            "message": "Login successful!",
            "username": active_user.username,
            "email": active_user.email,
        }

    async def test_login_handler_success_with_email(
        self, mock_db_session, active_user, plain_password
    ):
        """Handler returns success dict when valid email and password match."""
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = active_user
        login_data = LoginRequest(username=active_user.email, password=plain_password)

        result = await login(login_data=login_data, db=mock_db_session)

        mock_db_session.execute.assert_called_once()
        assert result == {
            "message": "Login successful!",
            "username": active_user.username,
            "email": active_user.email,
        }

    async def test_login_handler_user_not_found(self, mock_db_session):
        """Handler raises 401 HTTPException when user does not exist in DB."""
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = None
        login_data = LoginRequest(username="unknown_user", password="some_password")

        with pytest.raises(HTTPException) as exc_info:
            await login(login_data=login_data, db=mock_db_session)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Incorrect username or password."
        assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}

    async def test_login_handler_wrong_password(
        self, mock_db_session, active_user
    ):
        """Handler raises 401 HTTPException when password does not match hash."""
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = active_user
        login_data = LoginRequest(username=active_user.username, password="wrong_password")

        with pytest.raises(HTTPException) as exc_info:
            await login(login_data=login_data, db=mock_db_session)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Incorrect username or password."
        assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}

    async def test_login_handler_inactive_user(
        self, mock_db_session, inactive_user, plain_password
    ):
        """Handler raises 400 HTTPException when user account is inactive."""
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = inactive_user
        login_data = LoginRequest(username=inactive_user.username, password=plain_password)

        with pytest.raises(HTTPException) as exc_info:
            await login(login_data=login_data, db=mock_db_session)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == "Inactive account."
