from typing import TypedDict


class HawkCatcherSettings(TypedDict):
    """Settings for Hawk catcher for errors tracking"""

    token: str  # Hawk integration token
    host: str  # Collector hosts for sending event to
    secure: bool  # Use secure connection or not
    release: str  # Release name for Suspected Commits feature
