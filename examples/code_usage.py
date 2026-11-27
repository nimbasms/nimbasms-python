"""
Module example code usage:

This module provides examples for the main services of the Nimba SMS API.
"""

import os
import logging

from nimbasms import Client

ACCOUNT_SID = os.environ.get('NIMBA_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('NIMBA_AUTH_TOKEN')

client = Client(ACCOUNT_SID, AUTH_TOKEN)
logging.basicConfig(filename='./log.txt')
client.http_client.logger.setLevel(logging.INFO)


def check_balance():
    """Check the balances of the account."""
    response = client.accounts.get()
    if response.ok:
        account = response.data
        print(f"SMS balance : {account['sms_balance']}")
        print(f"WhatsApp balance : {account['whatsapp_balance']}")
        print(f"Email balance : {account['email_balance']}")


def get_purchases():
    """List the latest purchases."""
    response = client.purchases.list(limit=10)
    if response.ok:
        print(f"There are {response.data['count']} purchases")
        for purchase in response.data['results']:
            print(purchase)


def get_groups():
    """Get the groups list."""
    response = client.groups.list()
    if response.ok:
        print(f"There are {response.data['count']} groups")
        print(response.data['results'])


def get_sendernames():
    """Get validated sender names."""
    response = client.sendernames.list()
    if response.ok:
        for item in response.data['results']:
            print(item)


def add_contact():
    """Add contacts to the default list and to groups."""
    response = client.contacts.list()
    if response.ok:
        for contact in response.data['results']:
            print(contact)

    response = client.contacts.create(numero='+126456789')
    if response.ok:
        print(response.data)

    response = client.contacts.create(
        numero='+123456789', name='Foo', groups=['API', 'Facebook Client'])
    if response.ok:
        print(response.data)

    response = client.contacts.create(
        numero='+123456789', email='foo@example.com', groups=['API'])
    if response.ok:
        print(response.data)


def send_message():
    """Send and retrieve SMS messages."""
    print('Sending a message...')
    response = client.messages.create(
        to=['XXXX'], sender_name='YYYY', message='Hi Nimba!')
    if response.ok:
        print(f'message response : {response.data}')

    response = client.messages.get(messageid='XXXXXXXXXXXXXXXXXXXXX')
    if response.ok:
        print(f"Message retrieve : {response.data}")


def send_whatsapp_message():
    """Send a WhatsApp message with a validated template."""
    response = client.messages.create(
        to=['+123456789'], sender_name='Foo', channel='whatsapp',
        template_name='info',
        template_variables={'body': {'1': 'value 1', "2": 'value 2'}})
    if response.ok:
        print(f'WhatsApp response : {response.data}')
    else :
        print(response.data)


def send_email():
    """Send an email with an HTML version and an attachment."""
    response = client.messages.create(
        to=['client@example.com'], sender_name='YYYY', channel='email',
        subject='Your invoice', message='Plain text version',
        html='<p>HTML version</p>', reply_to=['support@example.com'],
        attachments=[{'filename': 'invoice.pdf', 'content': '<base64>'}])
    if response.ok:
        print(f'Email response : {response.data}')


def create_verification():
    """Request a verification code by SMS and by email."""
    response = client.verifications.create(
        to='+123456789', message='Your verification code is: <1234>',
        expiry_time=5)
    if response.ok:
        print(f"Verification request : {response.data}")

    response = client.verifications.create(
        channels=['email'], email='client@example.com',
        email_sender_name='no-reply@example.com')
    if response.ok:
        print(f"Email verification request : {response.data}")


def verify_code():
    """Check a verification code."""
    response = client.verifications.verify(
        verificationid='e132dc0f-2fa8-46f6-8d0b-1618bb74541f', code='41747')
    if response.ok:
        print(f"Verification result : {response.data}")
    else:
        print(response.data)


def list_extensions():
    """List the extensions available on the account."""
    response = client.extensions.list(limit=10)
    if response.ok:
        for extension in response.data['results']:
            print(extension)


def get_contacts():
    """List contacts."""
    response = client.contacts.list()
    if response.ok:
        for contact in response.data['results']:
            print(contact)


def retrieve_message():
    """Retrieve a message with the historical method name."""
    response = client.messages.retrieve(messageid='XXXXXXXXXXXXXXXXXXXXX')
    if response.ok:
        print(f"Message retrieve : {response.data}")


def create_verification_whatsapp():
    """Request a verification code by WhatsApp."""
    response = client.verifications.create(
        to='+123456789', channels=['whatsapp'], sender_name='YYYY')
    if response.ok:
        print(f"WhatsApp verification request : {response.data}")


def create_verification_multi_channel():
    """Request a verification code on several channels."""
    response = client.verifications.create(
        to='+123456789', channels=['sms', 'whatsapp', 'email'],
        sender_name='YYYY', whatsapp_sender_name='YYYY',
        email='client@example.com', email_sender_name='no-reply@example.com',
        email_template_name='verification', email_subject='Your verification code',
        expiry_time=10, attempts=3, code_length=6, language='en')
    if response.ok:
        print(f"Multi-channel verification request : {response.data}")


if __name__ == '__main__':
    check_balance()
    get_purchases()
    get_groups()
    get_sendernames()
    add_contact()
    send_message()
    send_whatsapp_message()
    send_email()
    create_verification()
    verify_code()
    list_extensions()
