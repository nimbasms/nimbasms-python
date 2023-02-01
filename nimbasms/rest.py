"""
A Nimba SMS Client Rest API.

This module contains Class Rest Client manager services.

Dependencies
-----------
List : Default library typing

class
---------
BaseRest : Abstract class representing rest client
Accounts: Account service.
Groups : Group Services.
SenderNames : Sender Name Services.
Contacts : Contact Services.
Messages : Messages Services.
"""

from typing import List


class BaseRest:
    """
    Base Rest client.
    """
    def __init__(self, client):
        """
        Iniatialize client rest with base url
        """
        self.base_url = 'https://api.nimbasms.com'
        self.client = client

    def __repr__(self):
        """
        Abstract Representing Serivce
        """
        raise NotImplementedError


class Accounts(BaseRest):
    """
    Manage Account Service.
    """
    def __init__(self, client):
        """
        Initialize Accounts
        """
        super().__init__(client)
        self.representation = '<Nimba.Accounts>'

    def __repr__(self):
        """
        Provide a friendly representation

        :returns Machine friendly representation
        :rtype: str
        """
        return self.representation

    def get(self):
        """
        Retrieve account information
        """
        return self.client.request(
            method='GET',
            uri=f'{self.base_url}/v1/accounts',
        )


class Groups(BaseRest):
    """
    Manage Group Service.
    """
    def __init__(self, client):
        """
        Initialize Groups
        """
        super().__init__(client)
        self._next = None
        self._previous = None
        self._count = 0

    def __repr__(self):
        """
        Provide a friendly representation

        :returns Machine friendly representation
        :rtype: str
        """
        return '<Nimba.Groups>'

    def request_message(self, uri, params=None):
        """
        Make HTTP request with Client.
        """
        response = self.client.request(
            method='GET',
            uri=uri,
            params=params or {}
        )
        if response.ok:
            self._next = response.data['next']
            self._previous =  response.data['previous']
            self._count = response.data['count']
        return response

    def next(self):
        """
        Paginate next data
        """
        if self._next is None:
            return None
        return self.request_message(self._next)

    def previous(self):
        """
        Paginate previous data
        """
        if self._previous is None:
            return None
        return self.request_message(self._previous)

    def list(self, limit: int=20, offset: int=0):
        """
        List messages

        :param int limit: Limit messages request
        :param int offset: offset to beging reqeust message
        """
        if not limit or limit < 0:
            raise ValueError('Limit must be positive Integer')
        if offset < 0:
            raise ValueError('Offset must be greater than 1')
        uri=f'{self.base_url}/v1/groups'
        return self.request_message(uri, {
            'limit': limit,
            'offset': offset
        })


class SenderNames(BaseRest):
    """
    Manager SenderName service.
    """
    def __init__(self, client):
        """
        Initialize SenderName
        """
        super().__init__(client)
        self._next = None
        self._previous = None
        self._count = 0

    def __repr__(self):
        """
        Provide a friendly representation

        :returns Machine friendly representation
        :rtype: str
        """
        return '<Nimba.SenderNames>'

    def request_message(self, uri, params=None):
        """
        Make HTTP request with Client.
        """
        response = self.client.request(
            method='GET',
            uri=uri,
            params=params or {}
        )
        if response.ok:
            self._next = response.data['next']
            self._previous =  response.data['previous']
            self._count = response.data['count']
        return response

    def next(self):
        """
        Paginate next data
        """
        if self._next is None:
            return None
        return self.request_message(self._next)

    def previous(self):
        """
        Paginate previous data
        """
        if self._previous is None:
            return None
        return self.request_message(self._previous)

    def list(self, limit: int=20, offset: int=0):
        """
        List sendername

        :param int limit: Limit sendernames request
        :param int offset: offset to beging reqeust message
        """
        if not limit or limit < 0:
            raise ValueError('Limit must be positive Integer')
        if offset < 0:
            raise ValueError('Offset must be greater than 1')
        uri=f'{self.base_url}/v1/sendernames'
        return self.request_message(uri, {
            'limit': limit,
            'offset': offset
        })


class Contacts(BaseRest):
    """
    Manage Contact service.
    """
    def __init__(self, client):
        """
        Initialize SenderName
        """
        super().__init__(client)
        self._next = None
        self._previous = None
        self._count = 0

    def __repr__(self):
        """
        Provide a friendly representation

        :returns Machine friendly representation
        :rtype: str
        """
        return '<Nimba.Contacts>'

    def request_message(self, uri, params=None):
        """
        Make HTTP request with Client.
        """
        response = self.client.request(
            method='GET',
            uri=uri,
            params=params or {}
        )
        if response.ok:
            self._next = response.data['next']
            self._previous =  response.data['previous']
            self._count = response.data['count']
        return response

    def next(self):
        """
        Paginate next data
        """
        if self._next is None:
            return None
        return self.request_message(self._next)

    def previous(self):
        """
        Paginate previous data
        """
        if self._previous is None:
            return None
        return self.request_message(self._previous)

    def list(self, limit: int=20, offset: int=0):
        """
        List contacts

        :param int limit: Limit contacts request
        :param int offset: offset to beging reqeust message
        """
        if not limit or limit < 0:
            raise ValueError('Limit must be positive Integer')
        if offset < 0:
            raise ValueError('Offset must be greater than 1')
        uri=f'{self.base_url}/v1/contacts'
        return self.request_message(uri, {
            'limit': limit,
            'offset': offset
        })

    def create(self, numero: str, name: str=None, groups: List[str]=None):
        """
        Create message for sending sms

        :param str to: List contact receiver
        :param str sender_name: Sender Name, is Sensitive Case
        :param str message: Text message
        """
        data = {'numero': numero}
        if name:
            data['name'] = name
        if groups:
            data['groups'] = groups
        return self.client.request(
            method='POST',
            uri=f'{self.base_url}/v1/contacts',
            data=data
        )


class Messages(BaseRest):
    """
    Manage Message Service.
    """
    def __init__(self, client):
        """
        Initialize Messages
        """
        super().__init__(client)
        self._next = None
        self._previous = None
        self._count = 0

    def __repr__(self):
        """
        Provide a friendly representation

        :returns Machine friendly representation
        :rtype: str
        """
        return '<Nimba.Messages>'

    def create(self, to: List[str], sender_name: str, message: str):
        """
        Create message for sending sms

        :param list to: List contact receiver
        :param str sender_name: Sender Name, is Sensitive Case
        :param str message: Text message
        """
        return self.client.request(
            method='POST',
            uri=f'{self.base_url}/v1/messages',
            data={
                'to': to,
                'sender_name': sender_name,
                'message': message
            }
        )

    def request_message(self, uri, params=None):
        """
        Make HTTP request with Client.
        """
        response = self.client.request(
            method='GET',
            uri=uri,
            params=params or {}
        )
        if response.ok:
            self._next = response.data['next']
            self._previous =  response.data['previous']
            self._count = response.data['count']
        return response

    def next(self):
        """
        Paginate next data
        """
        if self._next is None:
            return None
        return self.request_message(self._next)

    def previous(self):
        """
        Paginate previous data
        """
        if self._previous is None:
            return None
        return self.request_message(self._previous)

    def list(self, limit: int=20, offset: int=0):
        """
        List messages

        :param int limit: Limit messages request
        :param int offset: offset to beging reqeust message
        """
        if not limit or limit < 0:
            raise ValueError('Limit must be positive Integer')
        if offset < 0:
            raise ValueError('Offset must be greater than 1')
        uri=f'{self.base_url}/v1/messages'
        return self.request_message(uri, {
            'limit': limit,
            'offset': offset
        })

    def retrieve(self, messageid):
        """
        Retrieve a message

        :parm str messageid: Id message
        """
        return self.client.request(
            method='GET',
            uri=f'{self.base_url}/v1/messages/{messageid}',
        )
