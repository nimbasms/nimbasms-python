"""
A Nimba SMS Client API.

This module contains the public objects of the client. Service managers
live in :mod:`nimbasms.resources`, the HTTP layer in :mod:`nimbasms.http`
and the client itself in :mod:`nimbasms.client`.
"""

from nimbasms.client import Client
from nimbasms.exceptions import NimbaSMSException
from nimbasms.http import HttpClient
from nimbasms.http import NimbaHttpClient
from nimbasms.http import Response
from nimbasms.version import __version__

__all__ = [
    'Client',
    'HttpClient',
    'NimbaHttpClient',
    'NimbaSMSException',
    'Response',
    '__version__',
]
