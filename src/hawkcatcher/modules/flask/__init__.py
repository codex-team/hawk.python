from .flask import HawkFlask
from .types import HawkCatcherSettings

hawk = HawkFlask()


def init(*args, **kwargs):
    hawk.init(*args, **kwargs)


def send(*args, **kwargs):
    hawk.send(*args, **kwargs)
