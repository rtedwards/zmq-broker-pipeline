import logging
from pathlib import Path
import sys
from time import gmtime

try:
    import coloredlogs
except ImportError:
    pass


def setup_logger(filename: str) -> None:
    filename = Path(filename)
    if len(filename.parts) > 1:  # only affects 1st party filenames not 3rd party
        filename = filename.stem + filename.suffix

    message_format = "%(asctime)s.%(msecs)03d UTC [%(name)s] [%(process)d] %(levelname)s: %(message)s"
    logging.Formatter.converter = gmtime
    logger = logging.getLogger(filename)

    if "coloredlogs" in sys.modules:

        coloredlogs.install(fmt=message_format, datefmt="%Y-%m-%d %H:%M:%S", stream=sys.stdout)
    else:
        logging.basicConfig(level=logging.INFO, format=message_format, datefmt="%Y-%m-%d %H:%M:%S", stream=sys.stdout)

    return logger
