"""Tests for the service managers."""

import os
import tempfile
import unittest

from nimbasms.http import Response
from nimbasms.resources import Accounts
from nimbasms.resources import Contacts
from nimbasms.resources import Extensions
from nimbasms.resources import Groups
from nimbasms.resources import Messages
from nimbasms.resources import Purchases
from nimbasms.resources import Verifications
from tests.helpers import RecordingClient
from tests.helpers import paginated

BASE = 'https://api.nimbasms.com/v1'


class AccountsTests(unittest.TestCase):
    """Test the account service."""

    def test_get(self):
        """Account information is read from the right endpoint."""
        client = RecordingClient(Response(200, '{"balance": 5}'))
        response = Accounts(client).get()
        self.assertEqual(response.data['balance'], 5)
        self.assertEqual(client.calls[0]['method'], 'GET')
        self.assertEqual(client.calls[0]['uri'], f'{BASE}/accounts')


class PaginationTests(unittest.TestCase):
    """Test the shared pagination logic."""

    def test_list_query_parameters(self):
        """Filters are merged with pagination parameters."""
        client = RecordingClient()
        Groups(client).list(limit=10, offset=5, name='VIP')
        self.assertEqual(client.calls[0]['params'], {
            'limit': 10,
            'offset': 5,
            'name': 'VIP',
        })

    def test_invalid_pagination(self):
        """Invalid limits and offsets are rejected before any request."""
        client = RecordingClient()
        groups = Groups(client)
        for limit, offset in ((0, 0), (-1, 0), (20, -1)):
            with self.assertRaises(ValueError):
                groups.list(limit=limit, offset=offset)
        self.assertEqual(client.calls, [])

    def test_next_uses_returned_url(self):
        """Next page follows the URL returned by the API."""
        client = RecordingClient(paginated(
            next_url=f'{BASE}/groups?offset=20', count=30))
        groups = Groups(client)
        groups.list()
        groups.next()
        self.assertEqual(client.calls[1]['uri'], f'{BASE}/groups?offset=20')

    def test_previous_uses_returned_url(self):
        """Previous page follows the URL returned by the API."""
        client = RecordingClient(paginated(
            previous=f'{BASE}/groups?offset=0', count=30))
        groups = Groups(client)
        groups.list()
        groups.previous()
        self.assertEqual(client.calls[1]['uri'], f'{BASE}/groups?offset=0')

    def test_managers_without_list_endpoint(self):
        """Managers without a GET list endpoint expose no list or pagination."""
        client = RecordingClient()
        for manager in (Messages(client), Verifications(client)):
            self.assertFalse(hasattr(manager, 'list'))
            self.assertFalse(hasattr(manager, 'next'))
            self.assertFalse(hasattr(manager, 'previous'))

    def test_non_paginated_body(self):
        """A plain list response does not break pagination."""
        client = RecordingClient(Response(200, '[{"contact_id": "x"}]'))
        contacts = Contacts(client)
        response = contacts.list()
        self.assertEqual(len(response.data), 1)
        self.assertIsNone(contacts.next())
        self.assertEqual(len(client.calls), 1)


class ContactsTests(unittest.TestCase):
    """Test the contact service."""

    def test_create_with_all_fields(self):
        """Contacts are created with their name and groups."""
        client = RecordingClient()
        Contacts(client).create(
            numero='224123456', name='Foo', groups=['API'])
        self.assertEqual(client.calls[0]['method'], 'POST')
        self.assertEqual(client.calls[0]['uri'], f'{BASE}/contacts')
        self.assertEqual(client.calls[0]['data'], {
            'numero': '224123456',
            'name': 'Foo',
            'groups': ['API'],
        })

    def test_create_with_email_only(self):
        """A contact can be created with an email address only."""
        client = RecordingClient()
        Contacts(client).create(email='foo@example.com')
        self.assertEqual(client.calls[0]['data'], {'email': 'foo@example.com'})

    def test_create_requires_number_or_email(self):
        """At least one contact detail is required."""
        client = RecordingClient()
        with self.assertRaises(ValueError):
            Contacts(client).create()
        self.assertEqual(client.calls, [])


class MessagesTests(unittest.TestCase):
    """Test the message service."""

    def test_create_sms_payload(self):
        """SMS messages keep the historical payload."""
        client = RecordingClient()
        Messages(client).create(
            to=['224123456'], sender_name='Nimba', message='Hello')
        self.assertEqual(client.calls[0]['data'], {
            'to': ['224123456'],
            'sender_name': 'Nimba',
            'message': 'Hello',
        })

    def test_create_email_payload(self):
        """Email messages carry their specific fields."""
        client = RecordingClient()
        Messages(client).create(
            to=['client@example.com'], sender_name='Nimba', message='text',
            channel='email', subject='Invoice', html='<p>Hello</p>',
            reply_to=['support@example.com'],
            attachments=[{'filename': 'invoice.pdf', 'content': 'Yg=='}],
            template_variables={'body': {'1': 'value'}})
        self.assertEqual(client.calls[0]['data'], {
            'to': ['client@example.com'],
            'sender_name': 'Nimba',
            'message': 'text',
            'channel': 'email',
            'subject': 'Invoice',
            'html': '<p>Hello</p>',
            'reply_to': ['support@example.com'],
            'attachments': [{'filename': 'invoice.pdf', 'content': 'Yg=='}],
            'template_variables': {'body': {'1': 'value'}},
        })

    def test_get_is_an_alias_of_retrieve(self):
        """Get and retrieve read the same endpoint."""
        client = RecordingClient()
        messages = Messages(client)
        messages.get('message-1')
        self.assertEqual(client.calls[0]['method'], 'GET')
        self.assertEqual(client.calls[0]['uri'], f'{BASE}/messages/message-1')


class VerificationsTests(unittest.TestCase):
    """Test the verification service."""

    def test_create_defaults(self):
        """Verification requests use the default message and code length."""
        client = RecordingClient()
        Verifications(client).create(to='+123456789')
        self.assertEqual(client.calls[0]['method'], 'POST')
        self.assertEqual(client.calls[0]['uri'], f'{BASE}/verifications')
        self.assertEqual(client.calls[0]['data'], {
            'to': '+123456789',
            'message': 'Code de vérification : <1234>',
            'code_length': 4,
        })

    def test_create_multiple_channels(self):
        """Verification requests can combine several channels."""
        client = RecordingClient()
        Verifications(client).create(
            channels=['sms', 'whatsapp', 'email'], email='foo@example.com',
            email_sender_name='no-reply@example.com', language='en')
        self.assertEqual(client.calls[0]['data'], {
            'channels': ['sms', 'whatsapp', 'email'],
            'email': 'foo@example.com',
            'email_sender_name': 'no-reply@example.com',
            'language': 'en',
            'message': 'Code de vérification : <1234>',
            'code_length': 4,
        })

    def test_verify(self):
        """Verification codes are checked with a PATCH request."""
        client = RecordingClient()
        Verifications(client).verify(verificationid='ver-1', code=1234)
        self.assertEqual(client.calls[0]['method'], 'PATCH')
        self.assertEqual(client.calls[0]['uri'], f'{BASE}/verifications/ver-1')
        self.assertEqual(client.calls[0]['data'], {'code': 1234})

    def test_verify_accepts_camel_case_identifier(self):
        """The camel case identifier alias is accepted."""
        client = RecordingClient()
        Verifications(client).verify(verificationId='ver-1', code='1234')
        self.assertEqual(client.calls[0]['uri'], f'{BASE}/verifications/ver-1')

    def test_verify_requires_identifier_and_code(self):
        """Identifier and code are both required."""
        client = RecordingClient()
        verifications = Verifications(client)
        with self.assertRaises(ValueError):
            verifications.verify(code=1234)
        with self.assertRaises(ValueError):
            verifications.verify(verificationid='ver-1')
        self.assertEqual(client.calls, [])


class PurchasesTests(unittest.TestCase):
    """Test the purchase service."""

    def test_list(self):
        """Purchases are listed with pagination parameters."""
        client = RecordingClient()
        Purchases(client).list(limit=10)
        self.assertEqual(client.calls[0]['method'], 'GET')
        self.assertEqual(client.calls[0]['uri'], f'{BASE}/purchases')
        self.assertEqual(client.calls[0]['params'], {'limit': 10, 'offset': 0})


class ExtensionsTests(unittest.TestCase):
    """Test the extension service."""

    def test_create_get_update_publish(self):
        """Extensions support creation, update and publication."""
        client = RecordingClient()
        extensions = Extensions(client)
        extensions.create(
            name='Shop', category='ecommerce', description='Shop extension',
            base_api_url='https://shop.example.com', auth_type='api_key',
            is_paid=False)
        extensions.get('ext-1')
        extensions.update('ext-1', description='Updated')
        extensions.publish('ext-1', False)
        self.assertEqual(client.calls[0]['method'], 'POST')
        self.assertEqual(client.calls[0]['uri'], f'{BASE}/extensions')
        self.assertEqual(client.calls[0]['data']['name'], 'Shop')
        self.assertEqual(client.calls[1]['method'], 'GET')
        self.assertEqual(client.calls[1]['uri'], f'{BASE}/extensions/ext-1')
        self.assertEqual(client.calls[2]['method'], 'PATCH')
        self.assertEqual(client.calls[2]['data'], {'description': 'Updated'})
        self.assertEqual(client.calls[3]['uri'], f'{BASE}/extensions/ext-1/publish')
        self.assertEqual(client.calls[3]['data'], {'is_published': False})

    def test_actions_lifecycle(self):
        """Extension actions support the full CRUD lifecycle."""
        client = RecordingClient()
        extensions = Extensions(client)
        extensions.list_actions('ext-1', limit=5)
        extensions.create_action(
            'ext-1', name='Orders', method='GET', endpoint='/orders',
            description='List orders')
        extensions.get_action('ext-1', 'action-1')
        extensions.update_action('ext-1', 'action-1', description='Updated')
        extensions.publish_action('ext-1', 'action-1')
        extensions.delete_action('ext-1', 'action-1')
        self.assertEqual(client.calls[0]['uri'], f'{BASE}/extensions/ext-1/actions')
        self.assertEqual(client.calls[0]['params'], {'limit': 5, 'offset': 0})
        self.assertEqual(client.calls[1]['method'], 'POST')
        self.assertEqual(client.calls[1]['data']['name'], 'Orders')
        self.assertEqual(client.calls[2]['method'], 'GET')
        self.assertEqual(client.calls[2]['uri'],
                         f'{BASE}/extensions/ext-1/actions/action-1')
        self.assertEqual(client.calls[3]['method'], 'PATCH')
        self.assertEqual(client.calls[3]['data'], {'description': 'Updated'})
        self.assertEqual(client.calls[4]['uri'],
                         f'{BASE}/extensions/ext-1/actions/action-1/publish')
        self.assertEqual(client.calls[4]['data'], {'is_published': True})
        self.assertEqual(client.calls[5]['method'], 'DELETE')

    def test_pricing_plans(self):
        """Pricing plans can be created, updated and deleted."""
        client = RecordingClient()
        extensions = Extensions(client)
        extensions.create_pricing_plan(
            'ext-1', name='Pro', price='10000', billing_period='monthly',
            features={'orders': 100})
        extensions.update_pricing_plan('ext-1', 'plan-1', price='15000')
        extensions.delete_pricing_plan('ext-1', 'plan-1')
        self.assertEqual(client.calls[0]['uri'],
                         f'{BASE}/extensions/ext-1/pricing-plans')
        self.assertEqual(client.calls[0]['data']['billing_period'], 'monthly')
        self.assertEqual(client.calls[1]['method'], 'PATCH')
        self.assertEqual(client.calls[1]['uri'],
                         f'{BASE}/extensions/ext-1/pricing-plans/plan-1')
        self.assertEqual(client.calls[2]['method'], 'DELETE')

    def test_upload_logo(self):
        """Extension logos are sent as multipart form data."""
        handle, path = tempfile.mkstemp(suffix='.png')
        os.close(handle)
        try:
            with open(path, 'wb') as logo:
                logo.write(b'fake')
            client = RecordingClient()
            Extensions(client).upload_logo('ext-1', path)
            self.assertEqual(client.calls[0]['method'], 'PATCH')
            self.assertEqual(client.calls[0]['uri'],
                             f'{BASE}/extensions/ext-1/logo')
            self.assertIn('logo', client.calls[0]['files'])
        finally:
            os.remove(path)


if __name__ == '__main__':
    unittest.main()
