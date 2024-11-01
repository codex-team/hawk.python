from hawkcatcher.types import HawkCatcherSettings, User
from typing import Callable, TypedDict
from flask import Request

class FlaskAddons(TypedDict):
    app: str  # name of flask app
    url: str # url of request
    method: str # method of request
    headers: dict # headers of request
    cookies: dict # cookies of request
    params: dict # request params
    form: dict # request form data
    json: dict # request json data

class Addons(TypedDict):
    flask: FlaskAddons

class FlaskSettings(HawkCatcherSettings):
    """Settings for Flask catcher for errors tracking"""

    set_user: Callable[[Request], User]  # This hook allows you to identify user
    with_addons: bool = True  # This parameter points if you want to send request data with error (cookies, headers, params, form, json)
