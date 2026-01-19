import pathlib
import requests
import datetime
from urllib.parse import quote

from exceptions import *
import os, logging

class PiHole:
    def __init__(self, host, password):
        self.host = host
        self.session_id = PiHole.login_with_password(host, password)
        self.encoded_session_id = quote(self.session_id)
        self.api_url = f"https://{self.host}/api"
        self.logger = logging.getLogger(__name__)

    def logout(self) -> str:
        auth_url = f"{self.api_url}/auth?sid={self.encoded_session_id}"
        response = requests.request("DELETE", auth_url, verify=False)
        return response.text

    def get_version(self) -> str:
        version_endpoint = f"{self.api_url}/info/version?sid={self.encoded_session_id}"
        response = self.send_request("GET", version_endpoint, verify=False)
        return response.get("version")

    def get_blocking_status(self) -> str:
        blocking_status_endpoint = f"{self.api_url}/dns/blocking?sid={self.encoded_session_id}"
        response = self.send_request("GET", blocking_status_endpoint, verify=False)
        return response.get("blocking")

    def set_blocking_status(self, blocking_status) -> str:
        blocking_status_endpoint = f"{self.api_url}/dns/blocking?sid={self.encoded_session_id}"
        response = self.send_request("POST", blocking_status_endpoint, json=blocking_status, verify=False)
        return response.get("blocking")

    def get_config(self) -> str:
        config_endpoint = f"{self.api_url}/config?sid={self.encoded_session_id}"
        response = self.send_request("GET", config_endpoint, verify=False)
        return response

    def get_backup(self, path_to_backup: pathlib.Path) -> None:
        teleport_endpoint = f"{self.api_url}/teleporter?sid={self.encoded_session_id}"
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(path_to_backup, f"{self.host}_{timestamp}_backup.zip")

        try:
            response = requests.get(teleport_endpoint, verify=False, timeout=100)
            response.raise_for_status()
        except requests.RequestException as e:
            raise PiHoleBackupError("Failed to download backup") from e

        try:
            os.makedirs(path_to_backup, exist_ok=True)
        except OSError as e:
            raise PiHoleBackupError(f"Cannot create directory: {path_to_backup}") from e

        try:
            with open(backup_file, "wb") as f:
                f.write(response.content)
        except OSError as e:
            raise PiHoleBackupError(f"Failed to save backup to {path_to_backup}") from e


    def update_gravity(self) -> None:
        gravity_url = f"{self.api_url}/action/gravity?sid={self.encoded_session_id}"
        try:
            response = requests.post(gravity_url, verify=False, timeout=100)
            response.raise_for_status()
        except requests.RequestException as e:
            raise PiHoleGravityUpdateError("Failed to update gravity") from e

    @staticmethod
    def send_request(method, url, **kwargs):

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
        except requests.RequestException as e:
            raise PiHoleAPIError(f"Failed to send request to {url}") from e

        try:
            return response.json()
        except ValueError as e:
            raise PiHoleAPIError(f"Invalid JSON response from {url}") from e

    @staticmethod
    def login_with_password(host, password):
        auth_url = f"https://{host}/api/auth"
        payload = {"password": password}

        try:
            response = PiHole.send_request("POST", auth_url, json=payload, verify=False)
        except PiHoleAPIError:
            raise PiHoleAPIError(f"Failed to login to {auth_url}")

        try:
            return response["session"]["sid"]
        except (KeyError, TypeError) as e:
            raise PiHoleAPIError("Login response missing session SID") from e