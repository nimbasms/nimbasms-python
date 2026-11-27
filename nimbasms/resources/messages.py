"""Message service."""

from typing import List

from nimbasms.resources.base import BaseRest


class Messages(BaseRest):
    """
    Manage Message Service.
    """
    def __init__(self, client):
        """
        Initialize Messages
        """
        super().__init__(client, 'messages')

    def create(self, to: List[str], sender_name: str, message: str=None,
               channel: str=None, subject: str=None, html: str=None,
               reply_to: List[str]=None, attachments: List[dict]=None,
               template_name: str=None, template_variables: dict=None):
        """
        Send a message through the sms, whatsapp or email channel

        :param list to: Recipients, phone numbers or email addresses
        :param str sender_name: Sender Name, is Sensitive Case
        :param str message: Text message, or plain text version of an email
        :param str channel: Delivery channel: sms, whatsapp or email
        :param str subject: Email subject
        :param str html: HTML version of an email
        :param list reply_to: Email reply-to addresses
        :param list attachments: Email attachments, base64 encoded
        :param str template_name: Validated template name, required for whatsapp
        :param dict template_variables: Variables used by the template
        """
        data = self.payload(
            to=to,
            sender_name=sender_name,
            message=message,
            channel=channel,
            subject=subject,
            html=html,
            reply_to=reply_to,
            attachments=attachments,
            template_name=template_name,
            template_variables=template_variables,
        )
        return self.request(method='POST', data=data)

    def list(self, limit=20, offset=0, sent_at=None, sent_at__lte=None,
             sent_at__gte=None):
        """
        List messages

        :param int limit: Limit messages request
        :param int offset: Offset to begin request
        :param str sent_at: Filter messages sent at a given date
        :param str sent_at__lte: Filter messages sent before a given date
        :param str sent_at__gte: Filter messages sent after a given date
        """
        return super().list(
            limit=limit,
            offset=offset,
            sent_at=sent_at,
            sent_at__lte=sent_at__lte,
            sent_at__gte=sent_at__gte,
        )

    def retrieve(self, messageid):
        """
        Retrieve a message

        :param str messageid: Id message
        """
        return self.request(
            method='GET',
            uri=f'{self.resource_url}/{messageid}',
        )

    def get(self, messageid):
        """
        Retrieve a message, alias of :meth:`retrieve`

        :param str messageid: Id message
        """
        return self.retrieve(messageid)
