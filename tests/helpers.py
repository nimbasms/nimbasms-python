"""Shared helpers for the unit tests."""

import json

from nimbasms.http import Response


class RecordingClient:
    """Fake client recording requests and returning queued responses."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, uri, params=None, data=None, **kwargs):
        """Record a request and return the next queued response."""
        self.calls.append({
            'method': method,
            'uri': uri,
            'params': params,
            'data': data,
            **kwargs,
        })
        if self.responses:
            return self.responses.pop(0)
        return paginated()


class RecordingHttpClient:
    """Fake HTTP client returning the arguments it received."""

    def __init__(self):
        self.calls = []

    def request(self, *args, **kwargs):
        """Record the call and return its arguments."""
        self.calls.append({'args': args, 'kwargs': kwargs})
        return {
            'method': args[0] if args else None,
            'uri': args[1] if len(args) > 1 else None,
            **kwargs,
        }


def paginated(results=None, next_url=None, previous=None, count=None):
    """Build a JSON response with pagination fields."""
    items = results or []
    body = {
        'count': count if count is not None else len(items),
        'next': next_url,
        'previous': previous,
        'results': items,
    }
    return Response(200, json.dumps(body))
