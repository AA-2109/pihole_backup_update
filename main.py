import logging
import os
from exceptions import PiHoleError
from pihole_cls import PiHole
from validation import set_config_params

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "backup_upgrade.log")
logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                    filename=LOG_FILE,
                    level=logging.INFO,
                    datefmt="[%Y-%m-%d %H:%M:%S]")


def main():
    password, ip_list, path_to_backup = set_config_params()
    pi_hole = None
    for host in ip_list:
        try:
            pi_hole = PiHole(host, password, path_to_backup)
            password = None
            pi_hole.get_backup()
            pi_hole.update_gravity()
            logger.info("[%s] Backup and Gravity update - successful", host)
        except PiHoleError:
            logger.exception("[%s] Backup and Gravity update - failed", host)

        finally:
            try:
                pi_hole.logout()
            except PiHoleError:
                logger.exception("Logout failed for %s", host)


if __name__ == "__main__":
    main()
