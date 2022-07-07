import logging
import sys
from multiprocessing import current_process
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def exit_program(exit_info: str):
    logger.error(exit_info)
    logger.info(f'Exiting {current_process().name}')
    sys.exit(1)
