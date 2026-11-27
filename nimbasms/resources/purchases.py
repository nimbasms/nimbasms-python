"""Purchase service."""

from nimbasms.resources.base import PaginatedRest


class Purchases(PaginatedRest):
    """
    Manage Purchase service.
    """
    def __init__(self, client):
        """
        Initialize Purchases
        """
        super().__init__(client, 'purchases')
