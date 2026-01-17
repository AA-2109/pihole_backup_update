from dotenv import load_dotenv
import os
from exceptions import ConfigurationError, ConfValidationError
import logging
import ipaddress
import pathlib

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate_ip_list(ip_list_raw: str | None) -> list[str]:
    if not ip_list_raw:
        raise ConfigurationError("IP_LIST not set")

    if not isinstance(ip_list_raw, str):
        raise TypeError("IP_LIST must be a string")

    ip_list = [ip.strip() for ip in ip_list_raw.split(",") if ip.strip()]
    if not ip_list:
        raise ConfValidationError("IP_LIST must contain at least one IP")

    for ip in ip_list:
        try:
            ipaddress.IPv4Address(ip)
        except ValueError as e:
            raise ConfValidationError(f"Invalid IP address: {ip}") from e

    return ip_list

def validate_password(password: str | None) -> str:
    if password is None:
        raise ConfigurationError("Password not set")

    if not isinstance(password, str):
        raise TypeError("Password must be a string")

    if len(password.strip()) < 1:
        raise ConfigurationError("Password can not be empty or whitespace only")

    return password

def validate_backup_path(path: str) -> pathlib.Path:
    if len(path.strip()) < 1:
        raise ConfigurationError("Path can not be empty or whitespace only")

    if not isinstance(path, str):
        raise TypeError("Path must be a string")

    path = pathlib.Path(path).expanduser().resolve()

    if not path.is_dir():
        raise ConfValidationError(f"Path is not directory: {path}")

    test_file = path / ".write_test"

    try:
        test_file.touch(exist_ok=False)
        test_file.unlink()
    except OSError as e:
        raise ConfValidationError(f"No write access to {path}") from e

    return path


def set_config_params() -> tuple[str, list[str], pathlib.Path]:
    password = os.getenv("PASSWORD")
    ip_list_raw = os.getenv("IP_LIST")
    path_to_backup = os.getenv("PATH_TO_BACKUP")

    if not path_to_backup:
        path_to_backup = "backup"

    valid_password = validate_password(password)

    valid_ip_list = validate_ip_list(ip_list_raw)

    valid_path_to_backup = validate_backup_path(path_to_backup)

    logger.info("Configuration loaded: IP_LIST=%s, PATH_TO_BACKUP=%s",
                valid_ip_list, valid_path_to_backup)

    return valid_password, valid_ip_list, valid_path_to_backup
