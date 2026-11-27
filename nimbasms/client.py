"""
Nimba SMS client.

This module holds the public :class:`Client` which exposes every service
manager exposed by the Nimba SMS API.
"""

import platform

from nimbasms.exceptions import NimbaSMSException
from nimbasms.http import NimbaHttpClient
from nimbasms.resources import Accounts
from nimbasms.resources import Contacts
from nimbasms.resources import Extensions
from nimbasms.resources import Groups
from nimbasms.resources import Messages
from nimbasms.resources import Purchases
from nimbasms.resources import SenderNames
from nimbasms.resources import Verifications
from nimbasms.version import __version__


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
        self._verifications = None
        self._purchases = None
        self._extensions = None

    def request(self, method, uri, params=None, data=None,
                     auth=None, headers=None, timeout=None, files=None):
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
        :param dict files: Files to send as multipart form data

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

        if data is not None and 'Content-Type' not in headers and not files:
            headers['Content-Type'] = 'application/json'

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
            files=files,
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

    @property
    def verifications(self):
        """
        Access the Verifications service.

        :returns Verifications NimbaAPI
        """
        if self._verifications is None:
            self._verifications = Verifications(self)
        return self._verifications

    @property
    def purchases(self):
        """
        Access the Purchases service.

        :returns Purchases NimbaAPI
        """
        if self._purchases is None:
            self._purchases = Purchases(self)
        return self._purchases

    @property
    def extensions(self):
        """
        Access the Extensions service.

        :returns Extensions NimbaAPI
        """
        if self._extensions is None:
            self._extensions = Extensions(self)
        return self._extensions
