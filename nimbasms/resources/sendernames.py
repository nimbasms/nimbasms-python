"""Sender name service."""

from nimbasms.resources.base import PaginatedRest


class SenderNames(PaginatedRest):
    """
    Manage SenderName service.
    """
    def __init__(self, client):
        """
        Initialize SenderName
        """
        super().__init__(client, 'sendernames')
