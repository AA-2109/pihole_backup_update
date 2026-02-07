import logging
import os
from dotenv import load_dotenv

load_dotenv()

def get_logger():
    logger = logging.getLogger(__name__)
    BASE_DIR = os.getenv("BASE_DIR", os.getcwd())
    LOG_FILE = os.path.join(BASE_DIR, "backup_upgrade.log")
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                    filename=LOG_FILE,
                    level=logging.INFO,
                    datefmt="[%Y-%m-%d %H:%M:%S]")
    return logger