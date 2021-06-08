from dataclasses import dataclass


@dataclass(frozen=True)
class Status:
    """The status or your API key."""

    remaining_requests: int
