import os

from nimbasms import Client

ACCOUNT_SID = os.environ.get('NIMBA_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('NIMBA_AUTH_TOKEN')


def example():
    """
    Some example usage of NIMBA SMS API with python client
    """
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Get your account balance
    response = client.accounts.get()
    if response.ok:
        my_account = response.data
        print('My Account balance : {}'.format(my_account['balance']))

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

    # Get messages in smaller pages...
    print('Sending a message...')
    response = client.messages.create(to=['XXXX'], sender_name='YYYY',
                    message='Hi Nimba!')
    if response.ok:
        print('message response : {}'.format(response.data))


def __name__ == '__main__':
    exemple()
