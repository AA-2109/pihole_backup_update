import requests
from dotenv import load_dotenv
from pihole_cls import PiHole
import os, json


load_dotenv()

def main():
    password = os.getenv("PASSWORD")
    if not password:
        raise RuntimeError("PASSWORD not set")

    ip_list = json.loads(os.getenv("IP_LIST", "[]"))
    if not ip_list:
        raise RuntimeError("IP_LIST not set")

    path_to_backup = os.getenv("PATH_TO_BACKUP") or "./backup"

    for host in ip_list:
        try:
            pi_hole = PiHole(host, password)
            pi_hole.get_backup(path_to_backup)
            pi_hole.update_gravity()
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error, check if your Pi-Hole is running and accessible\n Error: {e}")
        else:
            print(f"[{pi_hole.host}] Backup and Gravity update - successful")
        finally:
            pi_hole.logout()

if __name__ == "__main__":
    main()

