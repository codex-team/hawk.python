from hawk_python_sdk.types import HawkCatcherSettings, User, Addons
from typing import Callable, TypedDict
from flask import Request

class FlaskAddons(TypedDict):
    url: str # url of request
    method: str # method of request
    headers: dict # headers of request
    cookies: dict # cookies of request
    params: dict # request params
    form: dict # request form data
    json: dict # request json data

class Addons(Addons):
    flask: FlaskAddons

class FlaskSettings(HawkCatcherSettings[Request]):
    """Settings for Flask catcher for errors tracking"""
    pass
