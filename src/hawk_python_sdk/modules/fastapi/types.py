from hawk_python_sdk.types import HawkCatcherSettings, User, Addons
from typing import Callable, TypedDict
from starlette.applications import Starlette
from fastapi import Request

class FastapiAddons(TypedDict):
    url: str # url of request
    method: str # method of request
    headers: dict # headers of request
    cookies: dict # cookies of request
    params: dict # request params

class Addons(Addons):
    fastapi: FastapiAddons

class FastapiSettings(HawkCatcherSettings[Request]):
    """Settings for Fastapi catcher for errors tracking"""

    app_instance: Starlette # Fastapi app instance to add catching