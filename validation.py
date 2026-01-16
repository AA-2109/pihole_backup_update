from dotenv import load_dotenv
import os, json
from exceptions import ConfigurationError, ConfValidationError
import logging

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate_ip_list(ip_list_raw: str | None) -> list[str]:
    if not ip_list_raw:
        raise ConfigurationError("IP_LIST not set")

    try:
        ip_list = json.loads(ip_list_raw)
    except json.JSONDecodeError as e:
        raise ConfValidationError("IP_LIST must be valid JSON") from e

    if not isinstance(ip_list, list) or not all(isinstance(ip, str) for ip in ip_list):
        raise ConfValidationError("IP_LIST must be a list of strings")

    return ip_list

def validate_password(password: str | None) -> str:
    if password is None:
        raise ConfigurationError("Password not set")

    if len(password.strip()) < 1:
        raise ConfigurationError("Password can not be empty or whitespace only")

    return password

def prepare_backup_directory(path: str) -> str:
    path = os.path.abspath(os.path.expanduser(path))

    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        raise ConfValidationError(f"Cannot create directory: {path}") from e

    if not os.access(path, os.W_OK):
        raise ConfValidationError(f"No write access to {path}")

    return path


def set_config_params() -> tuple[str, list[str], str]:
    password = os.getenv("PASSWORD")
    ip_list_raw = os.getenv("IP_LIST")
    path_to_backup = os.getenv("PATH_TO_BACKUP")

    if not path_to_backup:
        path_to_backup = "./backup"

    valid_password = validate_password(password)

    valid_ip_list = validate_ip_list(ip_list_raw)

    valid_path_to_backup = prepare_backup_directory(path_to_backup)

    logger.info("Configuration loaded: IP_LIST=%s, PATH_TO_BACKUP=%s",
                valid_ip_list, valid_path_to_backup)

    return valid_password, valid_ip_list, valid_path_to_backup
