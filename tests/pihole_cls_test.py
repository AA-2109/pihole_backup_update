from pathlib import Path
from unittest import mock
import requests

import pytest
from unittest.mock import patch
from pihole_cls import PiHole
from exceptions import (PiHoleError,
                        PiHoleBackupError,
                        PiHoleAPIError,
                        PiHoleGravityUpdateError)


class TestPihole:
    @pytest.fixture
    def mock_login(self):
        with patch("pihole_cls.PiHole.login_with_password", return_value="hello World!"):
            yield

    @pytest.fixture
    def pihole(self, mock_login):
        return PiHole("127.0.0.1", "secret", Path("."))

    def test_init_sets_session_id(self, pihole):
        assert pihole.session_id == "hello World!"

    def test_init_sets_host_and_api_url(self, pihole):
        assert pihole.host == "127.0.0.1"
        assert pihole.api_url == "https://127.0.0.1/api"

    def test_init_encodes_session_id(self, pihole):
        assert pihole.encoded_session_id == "hello%20World%21"

    def test_init_logger_initialized(self, pihole):
        assert pihole.logger is not None

    @mock.patch("pihole_cls.PiHole.send_request")
    def test_login_raises_pihole_api_error(self, mock_send):
        mock_send.side_effect = PiHoleAPIError()
        with pytest.raises(PiHoleAPIError, match="Failed to login to https://127.0.0.1/api/auth"):
            PiHole.login_with_password("127.0.0.1", "secret")

    @mock.patch("pihole_cls.PiHole.send_request")
    def test_return_no_sid(self, mock_post):
        mock_post.return_value = {"session": {}}

        with pytest.raises(PiHoleAPIError, match="Login response missing session SID"):
            PiHole.login_with_password("127.1", "secret")

    @mock.patch("pihole_cls.requests.request")
    def test_failed_send_request(self, mock_request):
        auth_url = "https://127.0.0.1/api/auth"
        mock_request.side_effect = requests.RequestException("404")

        with pytest.raises(PiHoleAPIError, match=f"Failed to send request to {auth_url}"):
            PiHole.send_request("POST", auth_url)

    @mock.patch("pihole_cls.requests.request")
    def test_send_request_returns_not_JSON(self, mock_request):
        auth_url = "https://127.0.0.1/api/auth"
        mock_response = mock.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Not JSON")
        mock_request.return_value = mock_response

        with pytest.raises(PiHoleAPIError, match=f"Invalid JSON response from {auth_url}"):
            PiHole.send_request("POST", auth_url)

        mock_response.raise_for_status.assert_called_once()

    @mock.patch("pihole_cls.requests.post")
    def test_failed_gravity_update(self, mock_request, pihole):
        mock_request.side_effect = requests.RequestException("404")

        with pytest.raises(PiHoleGravityUpdateError, match="Failed to update gravity"):
            pihole.update_gravity()

    @mock.patch("pihole_cls.requests.post")
    def test_success_gravity_update(self, mock_request, pihole):
        mock_response = mock.Mock()
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        pihole.update_gravity()

        gravity_url = f"{pihole.api_url}/action/gravity?sid={pihole.encoded_session_id}"
        mock_request.assert_called_once_with(
            gravity_url,
            verify=False,
            timeout=100,
        )
        mock_response.raise_for_status.assert_called_once()

    @mock.patch("pihole_cls.requests.get")
    def test_failed_backup(self, mock_request, pihole):
        mock_request.side_effect = requests.RequestException("404")

        with pytest.raises(PiHoleBackupError, match="Failed to download backup"):
            pihole.get_backup()

    @mock.patch("pihole_cls.requests.get")
    @mock.patch("pihole_cls.os.makedirs")
    def test_failed_to_write_backup(self, mock_makedirs, mock_get, pihole):
        mock_response = mock.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"fake zip content"
        mock_get.return_value = mock_response
        mock_makedirs.side_effect = OSError("Permission denied")

        with pytest.raises(PiHoleBackupError, match=f"Cannot create directory: {pihole.path_to_backup}"):
            pihole.get_backup()