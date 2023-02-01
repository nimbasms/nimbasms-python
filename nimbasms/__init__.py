"""
A Nimba SMS Client API.

This module contains Class Client manager services available in API : developers.nimbasms.com

Dependencies
-----------
requests : A library for HTTP Request

class
---------
HTTPClient : Abstract class representing HTTP Client
Response: Response representing data output.
Client : Manager all services APIs.
"""

import logging
import platform
import json

from urllib.parse import urlencode
from requests import Request, Session, hooks
from requests.adapters import HTTPAdapter
from nimbasms.execptions import NimbaSMSException

from nimbasms.rest import Accounts
from nimbasms.rest import Contacts
from nimbasms.rest import Groups
from nimbasms.rest import Messages
from nimbasms.rest import SenderNames

__version__ = '1.0.0'

_logger = logging.getLogger('nimbasms')

class HttpClient:
    """
    An Abstract class representing an HTTP client.
    """
    def request(self, method, url, params=None, data=None, headers=None,
                auth=None, timeout=None):
        """
        Make an HTTP request.
        """
        raise NimbaSMSException('HttpClient is a an abstract class')


class Response:
    """
    Representing data output API calls.
    """
    def __init__(self, status_code, text, headers=None):
        self.content = text
        self.headers = headers
        self.cached = False
        self.status_code = status_code
        self.ok = self.status_code < 400

    @property
    def text(self):
        """
        Content output byte
        """
        return self.content

    @property
    def data(self):
        """
        Output data response APIs
        """
        return json.loads(self.content)

    def __repr__(self):
        return f'HTTP {self.status_code} {self.content}'


class NimbaHttpClient(HttpClient):
    """
    General purpose HTTP Client for interacting with Nimba SMS API
    """
    def __init__(self, pool_connections=True, request_hooks=None, timeout=None,
                logger=_logger, proxy=None, max_retries=None):
        """
        Constructor for the NimbaHttpClient

        :param bool pool_connections
        :param request_hooks
        :param int timeout: Timeout for the requests.
                            Timeout should never be zero (0) or less.
        :param logger
        :param dict proxy: Http proxy for the request session
        :param int max_retries: Maxium number of retries each request should
                                attempt
        """
        self.session = Session() if pool_connections else None
        if self.session and max_retries is not None:
            self.session.mount('https://', HTTPAdapter(max_retries=max_retries))
        self.last_request = None
        self.last_response = None
        self.logger = logger
        self.request_hooks = request_hooks or hooks.default_hooks()

        if timeout is not None and timeout <= 0:
            raise ValueError(timeout)
        self.timeout = timeout
        self.proxy = proxy if proxy else {}

    def request(self, method, url, params=None, data=None, headers=None,
                auth=None, timeout=None):
        """
        Make an HTTP Request with paramters provided.

        :param str mtehod: The HTTP method to use
        :param str url: The URL to request
        :param dict params: Query parameters to append to the URL
        :param dict data: Paramters to go in the body of the HTTP request
        :param dict headers: HTTP Headers to send with the request
        :param tuple auth: Basic Auth arguments
        :param float timeout: Socket/Read timeout for the request

        :return: An http response
        """
        if timeout is not None and timeout <= 0:
            raise ValueError(timeout)
        kwargs = {
            'method': method.upper(),
            'url': url,
            'params': params,
            'data': data,
            'headers': headers,
            'auth': auth,
            'hooks': self.request_hooks
        }
        self._log_request(kwargs)

        self.last_response = None
        session = self.session or Session()
        request = Request(**kwargs)
        self.last_request = None

        prepped_request = session.prepare_request(request)
        settings = session.merge_environment_settings(prepped_request.url,
                                self.proxy, None, None, None)
        settings['timeout'] = timeout if timeout is not None else self.timeout

        response = session.send(prepped_request, **settings)

        self._log_response(response)
        self.last_response = Response(int(response.status_code),
                                    response.text, response.headers)
        return self.last_response

    def _log_request(self, kwargs):
        """
        Logger request APIs
        """
        self.logger.info('-- BEGIN Nimba SMS API Request --')

        if kwargs['params']:
            self.logger.info(
                f"{kwargs['method']} Request: {kwargs['url']}?{urlencode(kwargs['params'])}")
            self.logger.info(f"Query Params: {kwargs['params']}")
        else:
            self.logger.info(f"{kwargs['method']} Request: {kwargs['url']}")

        if kwargs['headers']:
            self.logger.info('Headers:')
            for key, value in kwargs['headers'].items():
                #Do not log authorization headers
                if 'authorization' not in key.lower():
                    self.logger.info(f'{key} : {value}')

        self.logger.info('-- END Nimba SMS API Request --')

    def _log_response(self, response):
        self.logger.info(f'Response Status Code: {response.status_code}')
        self.logger.info(f'Response Headers: {response.headers}')


class Client:
    """A client for accessing the Nimba SMS API."""

    def __init__(self, account_sid=None, access_token=None):
        """
        Initializes the Nimba SMS Client

        :param str account_sid: Account SID
        :param str access_token: Token authenticate
        """
        if not account_sid or not access_token:
            raise NimbaSMSException("Credentials are required"
                    " to create a NimbaClient")
        self.auth = (account_sid, access_token)

        self.http_client = NimbaHttpClient()

        self._messages = None
        self._accounts = None
        self._contacts = None
        self._groups = None
        self._sendernames = None

    def request(self, method, uri, params=None, data=None,
                    auth=None, headers=None, timeout=None):
        """
        Makes a request to the Nimba API using the configured http client
        Authentication information is automatically added if none is provided

        :param str method: HTTP Method
        :param str uri: Fully qualified url
        :param dict[str, str] params: Query string parameters
        :param dict[str, str] data: POST body data
        :param dict[str, str] headers: HTTP Headers
        :param tuple(str, str) auth: Authentication
        :param int timeout: Timeout in seconds

        :returns: Response from the Nimba API
        """
        auth = auth or self.auth
        headers = headers or {}

        pkg_version = __version__
        os_name = platform.system()
        os_arch = platform.machine()
        python_version = platform.python_version()
        headers['User-Agent'] = (
            f'nimba-python/{pkg_version} ({os_name} {os_arch}) Python/{python_version}')
        headers['X-Nimba-Client'] = 'utf-8'

        if method == 'POST' and 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        if 'Accept' not in headers:
            headers['Accept'] = 'application/json'

        return self.http_client.request(
            method,
            uri,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            timeout=timeout,
        )

    @property
    def accounts(self):
        """
        Access the Accounts Nimba SMS

        :returns Accounts
        """
        if self._accounts is None:
            self._accounts = Accounts(self)
        return self._accounts

    @property
    def messages(self):
        """
        Message Accounts

        :returns Messages NimbaAPI
        """
        if self._messages is None:
            self._messages = Messages(self)
        return self._messages

    @property
    def contacts(self):
        """
        Contacts Contacts

        :returns Contacts NimbaAPI
        """
        if self._contacts is None:
            self._contacts = Contacts(self)
        return self._contacts

    @property
    def groups(self):
        """
        Group Accounts.

        :returns Groups NimbaAPI
        """
        if self._groups is None:
            self._groups = Groups(self)
        return self._groups

    @property
    def sendernames(self):
        """
        Sendername Accounts.

        :returns Sendername NimbaAPI
        """
        if self._sendernames is None:
            self._sendernames = SenderNames(self)
        return self._sendernames
