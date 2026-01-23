import os
import ipaddress
import pathlib
import pytest
import validation


from exceptions import ConfigurationError, ConfValidationError


class TestValidationUnit:
    def test_invalid_password(self):
        with pytest.raises(ConfigurationError):
            validation.validate_password("")

    def test_none_password(self):
        with pytest.raises(ConfigurationError):
            validation.validate_password(None)

    def test_whitespace_password(self):
        with pytest.raises(ConfigurationError):
            validation.validate_password(" ")

    def test_attribute_error(self):
        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            validation.validate_password(123)

    def test_valid_password(self):
        expected = "secret"
        result = validation.validate_password(expected)
        assert expected == result

    def test_password_is_string(self):
        result = validation.validate_password("secret")
        assert isinstance(result, str)

    def test_empty_ip_list(self):
        with pytest.raises(ConfigurationError):
            validation.validate_ip_list("")

    def test_whitespace_ip_list(self):
        with pytest.raises(ConfigurationError):
            validation.validate_ip_list(" ")

    def test_none_ip_list(self):
        with pytest.raises(ConfigurationError):
            validation.validate_ip_list(None)

    def test_comma_ip_list(self):
        with pytest.raises(ConfValidationError):
            validation.validate_ip_list(",,,")

    def test_not_full_ip_list(self):
        with pytest.raises(ConfValidationError):
            validation.validate_ip_list("129., ")

    def test_outside_ipv4_ip_list(self):
        with pytest.raises(ConfValidationError):
            validation.validate_ip_list("257.257.257.257")

    def test_ipv6_ip_list(self):
        with pytest.raises(ConfValidationError):
            validation.validate_ip_list("::1")

    def test_ip_list_not_str(self):
        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            validation.validate_ip_list(123)

    def test_valid_ip_list(self):
        result = validation.validate_ip_list('192.168.1.2, 192.168.1.3')
        assert isinstance(result, list)

    def test_return_ipv4_list(self):
        result = validation.validate_ip_list('192.168.1.2, 192.168.1.3')
        for ip in result:
            assert isinstance(ipaddress.ip_address(ip), ipaddress.IPv4Address)

    def test_path_to_file(self):
        with pytest.raises(ConfValidationError):
            validation.validate_backup_path("test.txt")

    def test_empty_path_to_folder(self):
        with pytest.raises(ConfigurationError):
            validation.validate_backup_path("")

    def test_none_path_to_folder(self):
        with pytest.raises(AttributeError):
            # noinspection PyTypeChecker
            validation.validate_backup_path(None)

    @pytest.mark.skipif(os.name == 'nt', reason="Unix specific test")
    def test_path_no_write_perm(self, tmp_path):
        tmp_path.chmod(0o555)
        with pytest.raises(ConfValidationError):
            validation.validate_backup_path(str(tmp_path))

    def test_valid_path(self):
        result = validation.validate_backup_path(".")
        assert isinstance(result, pathlib.Path)

    def test_valid_path_equals_expected_path(self):
        result = validation.validate_backup_path("./")
        expected_path = pathlib.Path("./").expanduser().resolve()
        assert result == expected_path
