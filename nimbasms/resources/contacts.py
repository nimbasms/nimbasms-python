"""Contact service."""

from typing import List

from nimbasms.resources.base import PaginatedRest


class Contacts(PaginatedRest):
    """
    Manage Contact service.
    """
    def __init__(self, client):
        """
        Initialize Contacts
        """
        super().__init__(client, 'contacts')

    def create(self, numero: str=None, name: str=None, groups: List[str]=None,
               email: str=None):
        """
        Create a contact

        A contact needs a phone number, an email address, or both.

        :param str numero: Contact phone number
        :param str name: Contact name, optional
        :param list groups: Groups to add the contact to, optional
        :param str email: Contact email address, optional
        """
        data = self.payload(numero=numero, name=name, groups=groups, email=email)
        if not data.get('numero') and not data.get('email'):
            raise ValueError('At least one of numero or email is required')
        return self.request(method='POST', data=data)
