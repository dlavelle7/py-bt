import logging
import sys

formatter = logging.Formatter(
    '%(asctime)s [%(name)s] %(levelname)s: %(message)s')

logger = logging.getLogger("py-bt")
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)
