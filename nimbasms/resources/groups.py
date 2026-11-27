"""Group service."""

from nimbasms.resources.base import PaginatedRest


class Groups(PaginatedRest):
    """
    Manage Group Service.
    """
    def __init__(self, client):
        """
        Initialize Groups
        """
        super().__init__(client, 'groups')
