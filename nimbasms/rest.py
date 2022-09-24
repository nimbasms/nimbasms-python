class Accounts(object):

    def __init__(self, client):
        """
        Initialize Accounts
        """
        self.base_url = 'http://api.dev.com:9001'
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

    def __repr__(self):
        """
        Provide a friendly representation

        :returns Machine friendly representation
        :rtype: str
        """
        return '<Nimba.Messages>'
