"""Purchase service."""

from nimbasms.resources.base import BaseRest


class Purchases(BaseRest):
    """
    Manage Purchase service.
    """
    def __init__(self, client):
        """
        Initialize Purchases
        """
        super().__init__(client, 'purchases')
