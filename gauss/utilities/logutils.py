import copy
import os
import sys
from contextlib import contextmanager

from loguru import logger as _logger

logger = _logger

logger.remove()

#  Set a temporary logger to handle only_sink=True (see context manager below.
_temp_logger = copy.deepcopy(logger)

#  Add default handler
logger.add(sys.stderr, diagnose=False)

#  Add the application-wide file sink with rotation capabilities
TMP_DIR_PATH = "/tmp/gauss_logs"
os.makedirs(TMP_DIR_PATH, exist_ok=True)
logger.add(f"{TMP_DIR_PATH}/run_{{time}}.log", diagnose=False, retention=10)

logger.opt(colors=True).info(f"Logging enabled. Last 10 logs available at <green>{TMP_DIR_PATH}</green>.")


#  Temporary sinks
@contextmanager
def temporary_add(*args, only_sink: bool = False, **kwargs):
    if only_sink:
        logger_ = _temp_logger
    else:
        logger_ = logger

    handle: int = logger_.add(*args, **kwargs)
    try:
        yield logger_
    finally:
        logger_.remove(handle)
