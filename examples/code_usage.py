import os
import logging

from nimbasms import Client

ACCOUNT_SID = os.environ.get('NIMBA_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('NIMBA_AUTH_TOKEN')


def example():
    """
    Some example usage of NIMBA SMS API with python client
    """
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    logging.basicConfig()
    logging.basicConfig(filename='./log.txt') # or loging in file
    client.http_client.logger.setLevel(logging.INFO)

    # Get your account balance
    response = client.accounts.get()
    if response.ok:
        my_account = response.data
        print('My Account balance : {}'.format(my_account['balance']))


    # Get groups
    response = client.groups.list()
    if response.ok:
        all_groups = response.data
        print('There are {} groupes'.format(len(all_messages)))


    # Get Sendernames
    response = client.sendernames.list()
    if response.ok:
        all_sendernames = response.data
        for item in all_sendernames:
            print(item)


    # Get Contact
    response = client.contacts.list()
    if response.ok:
        all_contacts = response.data
        for item in all_contacts:
            print(item)


    # Create Contact
    # This contact will be added to the default contact list
    response = client.contacts.create(numero='224XXXXXXXXX')
    if response.ok:
        contact = response.data
    # Create with groups and name - name and groups are optional.
    response = client.contacts.create(numero='224XXXXXXXXX', name='Foo', groups=['API', 'Facebook Client'])
    if response.ok:
        contact = response.data


    # Get All messages
    response = client.messages.list()
    if response.ok:
        all_messages = response.data
        print('There are {} messages in your account.'.format(len(all_messages)))

    # Get only last 10 messages
    response = client.messages.list(limit=10)
    if response.ok:
        some_messages = some_messages.data
        print('Here are the last 10 messages in your account:')
        for m in some_messages:
            print(m)

    # send message...
    print('Sending a message...')
    response = client.messages.create(to=['XXXX'],
                sender_name='YYYY', message='Hi Nimba!')
    if response.ok:
        print('message response : {}'.format(response.data))


    # Retrieve message
    response = client.messages.retrieve(messageid='XXXXXXXXXXXXXXXXXXXXX')
    if response.ok:
        print("Message retrieve : {}".format(response.data))


def __name__ == '__main__':
    exemple()
