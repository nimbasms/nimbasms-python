"""Tests for the public client and HTTP response wrapper."""

import unittest

from nimbasms import Client
from nimbasms import NimbaSMSException
from nimbasms import Response
from nimbasms.version import __version__
from tests.helpers import RecordingHttpClient


class ClientTests(unittest.TestCase):
    """Test the client configuration and headers."""

    def test_credentials_are_required(self):
        """Credentials are mandatory."""
        with self.assertRaises(NimbaSMSException):
            Client()
        with self.assertRaises(NimbaSMSException):
            Client('sid')
        with self.assertRaises(NimbaSMSException):
            Client(access_token='token')

    def test_managers_are_cached(self):
        """Managers are created once and reused."""
        client = Client('sid', 'token')
        for name in ('accounts', 'messages', 'contacts', 'groups',
                     'sendernames', 'verifications', 'purchases', 'extensions'):
            self.assertIs(getattr(client, name), getattr(client, name))
        self.assertEqual(
            client.messages.resource_url,
            'https://api.nimbasms.com/v1/messages',
        )

    def test_request_adds_authentication_and_headers(self):
        """Requests carry authentication and JSON headers."""
        client = Client('sid', 'token')
        client.http_client = RecordingHttpClient()
        result = client.request(
            'POST',
            'https://api.nimbasms.com/v1/messages',
            data={'to': ['224123456']},
        )
        self.assertEqual(result['method'], 'POST')
        self.assertEqual(result['auth'], ('sid', 'token'))
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertEqual(result['headers']['Accept'], 'application/json')
        self.assertIn(f'nimba-python/{__version__}', result['headers']['User-Agent'])
        self.assertNotIn('X-Nimba-Client', result['headers'])

    def test_multipart_request_does_not_set_content_type(self):
        """Multipart requests let requests set the content type."""
        client = Client('sid', 'token')
        client.http_client = RecordingHttpClient()
        result = client.request(
            'PATCH',
            'https://api.nimbasms.com/v1/extensions/1/logo',
            files={'logo': 'content'},
        )
        self.assertNotIn('Content-Type', result['headers'])
        self.assertEqual(result['files'], {'logo': 'content'})


class ResponseTests(unittest.TestCase):
    """Test the response wrapper."""

    def test_json_data(self):
        """JSON bodies are decoded."""
        response = Response(200, '{"balance": 10}')
        self.assertTrue(response.ok)
        self.assertEqual(response.data, {'balance': 10})
        self.assertEqual(response.text, '{"balance": 10}')

    def test_empty_and_plain_data(self):
        """Empty and non-JSON bodies do not raise."""
        self.assertIsNone(Response(204, '').data)
        self.assertEqual(Response(200, 'plain text').data, 'plain text')

    def test_error_status(self):
        """Error statuses are reported as not ok."""
        self.assertFalse(Response(400, '{"detail": "error"}').ok)


if __name__ == '__main__':
    unittest.main()
