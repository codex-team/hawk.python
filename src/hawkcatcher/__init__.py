__version__ = "3.4.1"

from .core import Hawk
from .types import HawkCatcherSettings
from .modules.flask.types import FlaskSettings

hawk = Hawk()


def init(*args, **kwargs):
    hawk.init(*args, **kwargs)


def send(*args, **kwargs):
    hawk.send(*args, **kwargs)