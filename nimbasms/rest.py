"""
A Nimba SMS Client Rest API.

This module keeps the historical import path for the service managers.
New code should import them from :mod:`nimbasms.resources`.
"""

from nimbasms import resources as _resources
from nimbasms.resources import Accounts
from nimbasms.resources import Contacts
from nimbasms.resources import Extensions
from nimbasms.resources import Groups
from nimbasms.resources import Messages
from nimbasms.resources import Purchases
from nimbasms.resources import SenderNames
from nimbasms.resources import Verifications

__all__ = _resources.__all__
