import logging
import sys

LOGGER = logging.getLogger("AnimeNewsBot")

LOGGER.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s | %(message)s",
    "%d-%m-%Y %H:%M:%S"
)

console = logging.StreamHandler(sys.stdout)
console.setFormatter(formatter)

LOGGER.handlers.clear()
LOGGER.addHandler(console)
