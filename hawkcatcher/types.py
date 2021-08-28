from typing import TypedDict, Callable


class HawkCatcherSettings(TypedDict):
    """Settings for Hawk catcher for errors tracking"""

    token: str  # Hawk integration token
    collector_endpoint: str  # Collector endpoint for sending event to
    release: str  # Release name for Suspected Commits feature
    before_send: Callable[[dict], None]  # This hook allows you to filter any data you don't want sending to Hawk
