from exceptions import PiHoleError
from pihole_cls import PiHole
from validation import set_config_params
from logger import get_logger



def main():
    password, ip_list, path_to_backup = set_config_params()
    pi_hole = None
    logger = get_logger()
    for host in ip_list:
        try:
            logger.info("Starting Upgrade and Backup routines for %s", host)
            pi_hole = PiHole(host, password, path_to_backup)
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

