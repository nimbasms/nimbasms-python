"""Account service."""

from nimbasms.resources.base import BaseRest


class Accounts(BaseRest):
    """
    Manage Account Service.
    """
    def __init__(self, client):
        """
        Initialize Accounts
        """
        super().__init__(client, 'accounts')

    def get(self):
        """
        Retrieve account information
        """
        return self.request(method='GET')
