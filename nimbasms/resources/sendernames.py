"""Sender name service."""

from nimbasms.resources.base import BaseRest


class SenderNames(BaseRest):
    """
    Manage SenderName service.
    """
    def __init__(self, client):
        """
        Initialize SenderName
        """
        super().__init__(client, 'sendernames')
