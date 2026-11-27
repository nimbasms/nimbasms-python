"""
HTTP layer for the Nimba SMS client.

This module contains the abstract HTTP client, its requests-based
implementation and the response wrapper returned by every API call.
"""

import json
import logging
import platform

from urllib.parse import urlencode
from requests import Request, Session, hooks
from requests.adapters import HTTPAdapter

from nimbasms.exceptions import NimbaSMSException
from nimbasms.version import __version__

_logger = logging.getLogger('nimbasms')


class HttpClient:
    """
    An Abstract class representing an HTTP client.
    """
    def request(self, method, url, params=None, data=None, headers=None,
                auth=None, timeout=None, files=None):
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
        Output data response APIs, or None for an empty body
        """
        if not self.content:
            return None
        try:
            return json.loads(self.content)
        except (TypeError, ValueError):
            return self.content

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
                auth=None, timeout=None, files=None):
        """
        Make an HTTP Request with paramters provided.

        :param str mtehod: The HTTP method to use
        :param str url: The URL to request
        :param dict params: Query parameters to append to the URL
        :param dict data: Paramters to go in the body of the HTTP request
        :param dict headers: HTTP Headers to send with the request
        :param tuple auth: Basic Auth arguments
        :param float timeout: Socket/Read timeout for the request
        :param dict files: Files to send as multipart form data

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
            'hooks': self.request_hooks,
            'files': files
        }
        if isinstance(data, (dict, list)):
            kwargs['json'] = data
            kwargs['data'] = None
        self._log_request(kwargs)

        self.last_response = None
        session = self.session or Session()
        request = Request(**kwargs)

        prepped_request = session.prepare_request(request)
        self.last_request = prepped_request
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
                if 'authorization' not in key.lower():
                    self.logger.info(f'{key} : {value}')

        self.logger.info('-- END Nimba SMS API Request --')

    def _log_response(self, response):
        self.logger.info(f'Response Status Code: {response.status_code}')
        self.logger.info(f'Response Headers: {response.headers}')
