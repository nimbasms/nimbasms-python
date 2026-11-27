"""Verification service."""

from nimbasms.resources.base import BaseRest


class Verifications(BaseRest):
    """
    Manage Verification service.

    Verification codes can be delivered by sms, whatsapp and email.
    """
    def __init__(self, client):
        """
        Initialize Verifications
        """
        super().__init__(client, 'verifications')

    def create(self, to=None, channels=None, sender_name=None,
               whatsapp_sender_name=None, email=None, email_sender_name=None,
               email_template_name=None, email_subject=None, message=None,
               expiry_time=None, attempts=None, code_length=None, language=None):
        """
        Request a verification code

        :param str to: Phone number receiving the code
        :param list channels: Delivery channels: sms, whatsapp and/or email
        :param str sender_name: Sender name for sms and whatsapp
        :param str whatsapp_sender_name: WhatsApp sender name
        :param str email: Email address receiving the code
        :param str email_sender_name: Verified email sender address
        :param str email_template_name: Email template containing {{code}}
        :param str email_subject: Email subject
        :param str message: Message containing the <1234> placeholder
        :param int expiry_time: Code validity in minutes, from 5 to 30
        :param int attempts: Maximum number of attempts, from 3 to 10
        :param int code_length: Code length, from 4 to 8
        :param str language: OTP template language: fr or en
        """
        data = self.payload(
            to=to,
            channels=channels,
            sender_name=sender_name,
            whatsapp_sender_name=whatsapp_sender_name,
            email=email,
            email_sender_name=email_sender_name,
            email_template_name=email_template_name,
            email_subject=email_subject,
            message=message,
            expiry_time=expiry_time,
            attempts=attempts,
            code_length=code_length,
            language=language,
        )
        data.setdefault('message', 'Code de vérification : <1234>')
        data.setdefault('code_length', 4)
        return self.request(method='POST', data=data)

    def verify(self, verificationid=None, code=None, verificationId=None):
        """
        Verify a verification code

        :param str verificationid: Id of the verification request
        :param code: Code received by the recipient
        :param str verificationId: Alias of verificationid
        """
        verificationid = verificationid or verificationId
        if not verificationid:
            raise ValueError('verificationid is required')
        if code is None:
            raise ValueError('code is required')
        return self.request(
            method='PATCH',
            uri=f'{self.resource_url}/{verificationid}',
            data={'code': code},
        )
