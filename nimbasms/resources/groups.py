"""Group service."""

from nimbasms.resources.base import BaseRest


class Groups(BaseRest):
    """
    Manage Group Service.
    """
    def __init__(self, client):
        """
        Initialize Groups
        """
        super().__init__(client, 'groups')
