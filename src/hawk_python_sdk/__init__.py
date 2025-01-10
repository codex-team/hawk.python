__version__ = "3.5.2"

from .core import Hawk
from .types import HawkCatcherSettings

hawk = Hawk()


def init(*args, **kwargs):
    hawk.init(*args, **kwargs)


def send(*args, **kwargs):
    hawk.send(*args, **kwargs)
