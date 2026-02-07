import logging
import os
from dotenv import load_dotenv

load_dotenv()


def get_logger():
    logger = logging.getLogger(__name__)
    base_dir = os.getenv("BASE_DIR", os.getcwd())
    log_file = os.path.join(base_dir, "backup_upgrade.log")
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", filename=log_file, level=logging.INFO,
                        datefmt="[%Y-%m-%d %H:%M:%S]")
    return logger
