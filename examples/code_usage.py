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

    response = client.contacts.create(numero='224XXXXXXXXX')
    if response.ok:
        print(response.data)

    response = client.contacts.create(
        numero='224XXXXXXXXX', name='Foo', groups=['API', 'Facebook Client'])
    if response.ok:
        print(response.data)

    response = client.contacts.create(
        numero='224XXXXXXXXX', email='foo@example.com', groups=['API'])
    if response.ok:
        print(response.data)


def send_message():
    """List, send and retrieve SMS messages."""
    response = client.messages.list()
    if response.ok:
        print(f"There are {response.data['count']} messages in your account.")

    response = client.messages.list(limit=10)
    if response.ok:
        for message in response.data['results']:
            print(message)

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
        to=['224XXXXXXXXX'], sender_name='YYYY', channel='whatsapp',
        template_name='my_template',
        template_variables={'body': {'1': 'value 1'}})
    if response.ok:
        print(f'WhatsApp response : {response.data}')


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
        verificationid='XXXXXXXXXXXXXXXXXXXXX', code='1234')
    if response.ok:
        print(f"Verification result : {response.data}")


def list_extensions():
    """List the extensions available on the account."""
    response = client.extensions.list(limit=10)
    if response.ok:
        for extension in response.data['results']:
            print(extension)


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
