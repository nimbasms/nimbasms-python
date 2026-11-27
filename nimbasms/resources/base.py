"""Base resource manager shared by every Nimba SMS service."""


class BaseRest:
    """
    Base Rest client.

    Holds the common request and pagination logic used by all service
    managers.
    """
    def __init__(self, client, resource):
        """
        Initialize client rest with base url.

        :param client: Client used to send the HTTP requests
        :param str resource: Name of the API resource
        """
        self.base_url = 'https://api.nimbasms.com'
        self.client = client
        self.resource = resource
        self._next = None
        self._previous = None
        self._count = 0

    @property
    def resource_url(self):
        """Fully qualified URL of the resource."""
        return f'{self.base_url}/v1/{self.resource}'

    def __repr__(self):
        """
        Provide a friendly representation

        :returns Machine friendly representation
        :rtype: str
        """
        return f'<Nimba.{self.__class__.__name__}>'

    @staticmethod
    def payload(**fields):
        """
        Build a request body without the fields left to None.
        """
        return {key: value for key, value in fields.items() if value is not None}

    @staticmethod
    def pagination(limit=20, offset=0):
        """
        Validate and build pagination query parameters.
        """
        if not limit or limit < 0:
            raise ValueError('Limit must be positive Integer')
        if offset < 0:
            raise ValueError('Offset must be greater than 1')
        return {'limit': limit, 'offset': offset}

    def request(self, method, uri=None, params=None, data=None, files=None):
        """
        Make HTTP request with Client.

        :param str method: HTTP method
        :param str uri: Fully qualified url, defaults to the resource url
        :param dict params: Query parameters
        :param dict data: Body parameters
        :param dict files: Files to upload, used by multipart endpoints
        """
        return self.client.request(
            method=method,
            uri=uri or self.resource_url,
            params=params,
            data=data,
            files=files,
        )

    def list_url(self, url, params=None):
        """
        List a resource from a custom URL and store the pagination state.
        """
        return self.request_message(url, params or {})

    def request_message(self, uri, params=None):
        """
        Make HTTP request with Client and store the pagination state.
        """
        response = self.request(method='GET', uri=uri, params=params or {})
        self._update_pagination(response)
        return response

    def list(self, limit=20, offset=0, **filters):
        """
        List resources

        :param int limit: Limit resources request
        :param int offset: Offset to begin request
        :param filters: Additional query filters
        """
        params = self.pagination(limit, offset)
        params.update({key: value for key, value in filters.items()
                       if value is not None})
        return self.list_url(self.resource_url, params)

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

    def _update_pagination(self, response):
        """
        Store the pagination values returned by the API.
        """
        if not response.ok:
            return
        data = response.data
        if not isinstance(data, dict):
            return
        self._next = data.get('next')
        self._previous = data.get('previous')
        self._count = data.get('count', 0)
