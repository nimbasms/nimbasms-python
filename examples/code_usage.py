"""
Module example code usage:

Ce module fournit les fonctions nécessaires
pour envoyer des SMS via l'api Nimba SMS avec le SDK python.
"""

import os
import logging

from nimbasms import Client

ACCOUNT_SID = os.environ.get('NIMBA_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('NIMBA_AUTH_TOKEN')

client = Client(ACCOUNT_SID, AUTH_TOKEN)
logging.basicConfig()
logging.basicConfig(filename='./log.txt') # or loging in file
client.http_client.logger.setLevel(logging.INFO)

def check_balance():
    """
    Check balance sms
    """
    response = client.accounts.get()
    if response.ok:
        my_account = response.data
        print(f"My Account balance : {my_account['balance']}")


def get_groups():
    """
    get groups list
    """
    response = client.groups.list()
    if response.ok:
        all_groups = response.data
        print(f'There are {len(all_groups)} groupes')


def get_sendernames():
    """
    Get sendername validated
    """
    response = client.sendernames.list()
    if response.ok:
        all_sendernames = response.data
        for item in all_sendernames:
            print(item)


def add_contact():
    """
    process contact added
    """
    response = client.contacts.list()
    if response.ok:
        all_contacts = response.data
        for item in all_contacts:
            print(item)

    # This contact will be added to the default contact list
    response = client.contacts.create(numero='224XXXXXXXXX')
    if response.ok:
        print(response.data)
    # Create with groups and name - name and groups are optional.
    response = client.contacts.create(
        numero='224XXXXXXXXX', name='Foo', groups=['API', 'Facebook Client'])
    if response.ok:
        print(response.data)


def send_message():
    """
    Send message
    """
    response = client.messages.list()
    if response.ok:
        all_messages = response.data
        print(f'There are {len(all_messages)} messages in your account.')

    # Get only last 10 messages
    response = client.messages.list(limit=10)
    if response.ok:
        some_messages = response.data
        print('Here are the last 10 messages in your account:')
        for message in some_messages:
            print(message)

    # send message...
    print('Sending a message...')
    response = client.messages.create(to=['XXXX'],
                sender_name='YYYY', message='Hi Nimba!')
    if response.ok:
        print(f'message response : {response.data}')

    # Retrieve message
    response = client.messages.retrieve(messageid='XXXXXXXXXXXXXXXXXXXXX')
    if response.ok:
        print(f"Message retrieve : {response.data}")


if __name__ == '__main__':
    check_balance()
    get_groups()
    get_sendernames()
    add_contact()
    send_message()
