from .fastapi import HawkFastapi
from .types import HawkCatcherSettings
from .types import FastapiSettings

hawk = HawkFastapi()


def init(*args, **kwargs):
    hawk.init(*args, **kwargs)


def send(*args, **kwargs):
    hawk.send(*args, **kwargs)