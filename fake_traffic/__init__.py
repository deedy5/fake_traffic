import logging

from .fake_traffic import FakeTraffic
from .version import __version__

# A do-nothing logging handler
# https://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("fake_traffic").addHandler(logging.NullHandler())
