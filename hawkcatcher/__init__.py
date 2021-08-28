__version__ = "3.4.0"

from .core import Hawk
from .types import HawkCatcherSettings

hawk = Hawk()


def init(*args, **kwargs):
    hawk.init(*args, **kwargs)


def send(*args, **kwargs):
    hawk.send(*args, **kwargs)
