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
        return PiHole("127.0.0.1", "secret")

    def test_init_sets_session_id(self, pihole):
        assert pihole.session_id == "hello World!"

    def test_init_sets_host_and_api_url(self, pihole):
        assert pihole.host == "127.0.0.1"
        assert pihole.api_url == "https://127.0.0.1/api"

    def test_init_encodes_session_id(self, pihole):
        assert pihole.encoded_session_id == "hello%20World%21"

    def test_init_logger_initialized(self, pihole):
        assert pihole.logger is not None

    @patch("pihole_cls.requests.post")
    def test_login_raises_pihole_api_error(self, mock_post):
        mock_post.side_effect = ConnectionError("404")
        with pytest.raises(PiHoleAPIError):
            PiHole.login_with_password("https://127.1/api/auth", "secret")

    @patch("pihole_cls.requests.post")
    def test_return_no_sid(self, mock_post):
        mock_post.return_value.json.return_value = {"session": {}}
        with pytest.raises(PiHoleAPIError):
            PiHole.login_with_password("https://127.1/api/auth", "secret")



