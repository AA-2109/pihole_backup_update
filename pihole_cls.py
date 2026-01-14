import requests
import datetime
from urllib.parse import quote
import os

class PiHole:
    def __init__(self, host, password):
        self.host = host
        self.session_id = PiHole.login_with_password(host, password)
        self.encoded_session_id = quote(self.session_id)
        self.api_url = f"http://{self.host}/api"

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

    def get_backup(self, path_to_backup: str):
        teleport_endpoint = f"{self.api_url}/teleporter?sid={self.encoded_session_id}"
        current_time = datetime.datetime.now()
        response = requests.request("GET", teleport_endpoint, verify=False)
        if not os.path.exists(path_to_backup):
            os.makedirs(path_to_backup)
        with open(f"{path_to_backup}/{self.host}_{current_time}_backup.zip", "wb") as f:
            f.write(response.content)
        return response.status_code

    def update_gravity(self):
        gravity_url = f"{self.api_url}/action/gravity?sid={self.encoded_session_id}"
        response = requests.request("POST", gravity_url, verify=False)
        return response.status_code

    @staticmethod
    def send_request(method, url, **kwargs):
        req = requests.request(method, url, **kwargs)
        return req.json()

    @staticmethod
    def login_with_password(host, password):
        auth_url = f"http://{host}/api/auth"
        payload = {"password": password}

        response = PiHole.send_request("POST", auth_url, json=payload, verify=False)
        return response.get("session").get("sid")