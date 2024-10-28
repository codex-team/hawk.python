from hawkcatcher.types import HawkCatcherSettings
from typing import Callable
from flask import Request

class FlaskSettings(HawkCatcherSettings):
    """Settings for Flask catcher for errors tracking"""

    set_user: Callable[[Request], dict]  # This hook allows you to identify user
    with_request_data: bool = True  # This parameter points if you want to send request data with error (cookies, headers, params, form, json)