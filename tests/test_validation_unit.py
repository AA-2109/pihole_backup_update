from json import JSONDecodeError

import validation
import pytest

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
            validation.validate_password(123)

    def test_valid_password(self):
        assert validation.validate_password("secret") == "secret"

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

    def test_otside_IPV4_ip_list(self):
        with pytest.raises(ConfValidationError):
            validation.validate_ip_list("257.257.257.257")

    def test_IPV6_ip_list(self):
        with pytest.raises(ConfValidationError):
            validation.validate_ip_list("::1")

    def test_ip_list_not_str(self):
        with pytest.raises(TypeError):
            validation.validate_ip_list(123)

    def test_valid_ip_list(self):
        assert validation.validate_ip_list('192.168.1.2, 192.168.1.3') == ["192.168.1.2", "192.168.1.3"]

    def test_path_to_file(self):
        with pytest.raises(ConfValidationError):
            validation.validate_backup_path("test.txt")

    def test_empty_path_to_folder(self):
        with pytest.raises(ConfigurationError):
            validation.validate_backup_path("")

    def test_None_path_to_folder(self):
        with pytest.raises(AttributeError):
            validation.validate_backup_path(None)

    def test_path_no_write_perm(self, tmp_path):
        tmp_path.chmod(0o555)
        with pytest.raises(ConfValidationError):
            validation.validate_backup_path(str(tmp_path))

    def test_valid_path(self):
        assert validation.validate_backup_path("./test") == "test.txt"