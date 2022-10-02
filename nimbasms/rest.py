class Accounts(object):
    def __init__(self, client):
        """
        Initialize Accounts
        """
        self.base_url = 'https://api.nimbasms.com'
        self.client = client

    def __repr__(self):
        """
        Provide a friendly representation

        :returns Machine friendly representation
        :rtype: str
        """
        return '<Nimba.Accounts>'

    def get(self):
        """
        Retreive account information
        """
        return self.client.request(
            method='GET',
            uri='{}/v1/accounts'.format(self.base_url),
        )



class Messages(object):
    def __init__(self, client):
        """
        Initialize Messages
        """
        self.base_url = 'https://api.nimbasms.com'
        self.client = client
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
            uri='{}/v1/messages/'.format(self.base_url),
            data={
                'to': to,
                'sender_name': sender_name,
                'message': message
            }
        )

    def request_message(self, uri, params={}):
        response = self.client.request(
            method='GET',
            uri=uri
        )
        if response.ok:
            self._next = response.data['next']
            self._previous =  response.data['previous']
            self._count = response.data['count']
        return response

    def list(self, limit:int=20, offset:int=1):
        """
        List messages

        :param int limit: Limit messages request
        :param int offset: offset to beging reqeust message
        """
        if not limit or limit <= 0:
            raise ValueError('Limit must be positive Integer')
        if offset < 1:
            raise ValueError('Offset must be greater than 1')
        uri='{}/v1/messages/'.format(self.base_url)
        return self.request_message(uri, {
            'limit': limit,
            'offset': offset
        })

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

    def retreive(self, messageid):
        """
        Retreive a message

        :parm str messageid: Id message
        """
        uri = '{}/v1/messages/{}'.format(
            self.base_url, messageid
        )
        return self.request_message(uri)
