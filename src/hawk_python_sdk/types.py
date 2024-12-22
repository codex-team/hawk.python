from typing import TypedDict, Callable, TypeVar, Generic


T = TypeVar('T')


class User(TypedDict):
    """User data for sending with event"""

    id: str # Internal user's identifier inside an app
    name: str # User public name
    image: str # User's public picture
    url: str # URL for user's details page

class HawkCatcherSettings(TypedDict, Generic[T]):
    """Settings for Hawk catcher for errors tracking"""

    token: str  # Hawk integration token
    collector_endpoint: str  # Collector endpoint for sending event to
    release: str  # Release name for Suspected Commits feature
    before_send: Callable[[dict], None]  # This hook allows you to filter any data you don't want sending to Hawk
    context: dict  # Additional context to be send with event
    with_addons: bool = True  # This parameter points if you want to send framework data with error (cookies, headers, params, form, json)
    set_user: Callable[[T], User] # This hook allows you to set user information, this hook is useful for frameworks

class Addons(TypedDict):
    """Additional data to be send with event due to frameworks"""
    pass