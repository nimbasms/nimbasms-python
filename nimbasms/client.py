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
        self._resources = {}

    def _manager(self, name, manager):
        """
        Return a cached service manager.

        :param str name: Name of the service
        :param manager: Manager class to instantiate
        """
        if name not in self._resources:
            self._resources[name] = manager(self)
        return self._resources[name]

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
        return self._manager('accounts', Accounts)

    @property
    def messages(self):
        """
        Message Accounts

        :returns Messages NimbaAPI
        """
        return self._manager('messages', Messages)

    @property
    def contacts(self):
        """
        Contacts Contacts

        :returns Contacts NimbaAPI
        """
        return self._manager('contacts', Contacts)

    @property
    def groups(self):
        """
        Group Accounts.

        :returns Groups NimbaAPI
        """
        return self._manager('groups', Groups)

    @property
    def sendernames(self):
        """
        Sendername Accounts.

        :returns Sendername NimbaAPI
        """
        return self._manager('sendernames', SenderNames)

    @property
    def verifications(self):
        """
        Access the Verifications service.

        :returns Verifications NimbaAPI
        """
        return self._manager('verifications', Verifications)

    @property
    def purchases(self):
        """
        Access the Purchases service.

        :returns Purchases NimbaAPI
        """
        return self._manager('purchases', Purchases)

    @property
    def extensions(self):
        """
        Access the Extensions service.

        :returns Extensions NimbaAPI
        """
        return self._manager('extensions', Extensions)
