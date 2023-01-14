from typing import List


class BaseRest(object):
    def __init__(self, client):
        self.base_url = 'https://api.nimbasms.com'
        self.client = client

    def __repr__(self):
        raise NotImplementedError


class Accounts(BaseRest):
    def __init__(self, client):
        """
        Initialize Accounts
        """
        super(Accounts, self).__init__(client)

    def __repr__(self):
        """
        Provide a friendly representation

        :returns Machine friendly representation
        :rtype: str
        """
        return '<Nimba.Accounts>'

    def get(self):
        """
        Retrieve account information
        """
        return self.client.request(
            method='GET',
            uri='{}/v1/accounts'.format(self.base_url),
        )


class Groups(BaseRest):
    def __init__(self, client):
        """
        Initialize Groups
        """
        super(Groups, self).__init__(client)
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

    def request_message(self, uri, params={}):
        response = self.client.request(
            method='GET',
            uri=uri,
            params=params
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
        if offset < 1:
            raise ValueError('Offset must be greater than 1')
        uri='{}/v1/groups'.format(self.base_url)
        return self.request_message(uri, {
            'limit': limit,
            'offset': offset
        })


class SenderNames(BaseRest):
    def __init__(self, client):
        """
        Initialize SenderName
        """
        super(SenderNames, self).__init__(client)
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

    def request_message(self, uri, params={}):
        response = self.client.request(
            method='GET',
            uri=uri,
            params=params
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
        if offset < 1:
            raise ValueError('Offset must be greater than 1')
        uri='{}/v1/sendernames'.format(self.base_url)
        return self.request_message(uri, {
            'limit': limit,
            'offset': offset
        })


class Contacts(BaseRest):
    def __init__(self, client):
        """
        Initialize SenderName
        """
        super(Contacts, self).__init__(client)
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

    def request_message(self, uri, params={}):
        response = self.client.request(
            method='GET',
            uri=uri,
            params=params
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

    def list(self, limit: int=20, offset: int=1):
        """
        List contacts

        :param int limit: Limit contacts request
        :param int offset: offset to beging reqeust message
        """
        if not limit or limit < 0:
            raise ValueError('Limit must be positive Integer')
        if offset < 1:
            raise ValueError('Offset must be greater than 1')
        uri='{}/v1/contacts'.format(self.base_url)
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
            uri='{}/v1/contacts'.format(self.base_url),
            data=data
        )


class Messages(BaseRest):
    def __init__(self, client):
        """
        Initialize Messages
        """
        super(Messages, self).__init__(client)
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

    def create(self, to:list, sender_name:str, message:str):
        """
        Create message for sending sms

        :param list to: List contact receiver
        :param str sender_name: Sender Name, is Sensitive Case
        :param str message: Text message
        """
        return self.client.request(
            method='POST',
            uri='{}/v1/messages'.format(self.base_url),
            data={
                'to': to,
                'sender_name': sender_name,
                'message': message
            }
        )

    def request_message(self, uri, params={}):
        response = self.client.request(
            method='GET',
            uri=uri,
            params=params
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
        if offset < 1:
            raise ValueError('Offset must be greater than 1')
        uri='{}/v1/messages'.format(self.base_url)
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
            uri='{}/v1/messages/{}'.format(self.base_url, messageid),
        )
