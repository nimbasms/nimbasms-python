# nimbasms-python

A Python module for communicating with the Nimba SMS API.

# Usage

 - [Installation](#installation)
 - [Check balance](#account)
 - [Purchases](#purchases)
 - [Groups](#group)
 - [Sendernames](#sendername)
 - [Create Contacts](#contact)
 - [Send Message](#message)
 - [Verifications](#verifications)
 - [Extensions](#extensions)
 - [Logs Activities](#log)

## <a name="installation"></a> Installation

```sh
pip install nimbasms
```

Every example starts by creating a client with your API credentials:

```python
from nimbasms import Client

ACCOUNT_SID = 'XXXX'
AUTH_TOKEN = 'XXXX'
client = Client(ACCOUNT_SID, AUTH_TOKEN)
```

## <a name="account"></a> Check balance

```python
response = client.accounts.get()
if response.ok:
    account = response.data
    print('SMS balance : {}'.format(account['sms_balance']))
    print('WhatsApp balance : {}'.format(account['whatsapp_balance']))
    print('Email balance : {}'.format(account['email_balance']))
```

## <a name="purchases"></a> Purchases

```python
response = client.purchases.list(limit=10)
if response.ok:
    purchases = response.data
    print('There are {} purchases'.format(purchases['count']))
    for purchase in purchases['results']:
        print(purchase)

next_page = client.purchases.next()
previous_page = client.purchases.previous()
```

Paginated endpoints return `count`, `next`, `previous` and `results`.
`next()` and `previous()` return `None` when there is no more page.

## <a name="group"></a> Groups

```python
response = client.groups.list()
if response.ok:
    groups = response.data
    print('There are {} groups'.format(groups['count']))
    for group in groups['results']:
        print(group)
```

## <a name="sendername"></a> Sendernames

```python
response = client.sendernames.list()
if response.ok:
    sendernames = response.data
    for item in sendernames['results']:
        print(item)
```

## <a name="contact"></a> Create Contact

```python
response = client.contacts.list()
if response.ok:
    for contact in response.data['results']:
        print(contact)

# This contact will be added to the default contact list
response = client.contacts.create(numero='224XXXXXXXXX')
if response.ok:
    contact = response.data

# Create with groups and name - name and groups are optional
response = client.contacts.create(
    numero='224XXXXXXXXX', name='Foo', groups=['API', 'Facebook Client'])

# A contact can also be created with an email address
response = client.contacts.create(
    numero='224XXXXXXXXX', name='Foo', email='foo@example.com', groups=['API'])
```

## <a name="message"></a> Send message

```python
# Get all messages
response = client.messages.list()
if response.ok:
    print('There are {} messages'.format(response.data['count']))

# Get the last 10 messages, optionally filtered by date
response = client.messages.list(limit=10, sent_at__gte='2026-01-01T00:00:00Z')
if response.ok:
    for message in response.data['results']:
        print(message)

# Send an SMS
response = client.messages.create(
    to=['224XXXXXXXXX'], sender_name='YYYY', message='Hi Nimba!')

# Send a WhatsApp message with a validated template
response = client.messages.create(
    to=['224XXXXXXXXX'], sender_name='YYYY', channel='whatsapp',
    template_name='my_template',
    template_variables={'body': {'1': 'value 1', '2': 'value 2'}})

# Send an email with an HTML version, a reply-to address and attachments
response = client.messages.create(
    to=['client@example.com'], sender_name='YYYY', channel='email',
    subject='Your invoice', message='Plain text version of the email',
    html='<p>HTML version of the email</p>',
    reply_to=['support@example.com'],
    attachments=[{'filename': 'invoice.pdf', 'content': '<base64>'}])

# Retrieve a message
response = client.messages.get(messageid='XXXXXXXXXXXXXXXXXXXXX')
if response.ok:
    print('Message retrieved : {}'.format(response.data))
```

`retrieve()` remains available as an alias of `get()`.

## <a name="verifications"></a> Verifications

```python
# Send a verification code by SMS
response = client.verifications.create(
    to='+123456789', message='Your verification code is: <1234>', expiry_time=5)

# The default message and a 4-digit code are used when omitted
response = client.verifications.create(to='+123456789')

# Check the code received by the recipient
response = client.verifications.verify(
    verificationid='XXXXXXXXXXXXXXXXXXXXX', code='1234')

# Ask for the code on WhatsApp
response = client.verifications.create(
    to='+123456789', channels=['whatsapp'], sender_name='YYYY')

# Ask for the code by email
response = client.verifications.create(
    channels=['email'], email='client@example.com',
    email_sender_name='no-reply@example.com',
    email_subject='Your verification code')
```

Channels can be combined, for example `channels=['sms', 'whatsapp', 'email']`.

## <a name="extensions"></a> Extensions

```python
# List extensions
response = client.extensions.list(limit=10)
if response.ok:
    for extension in response.data['results']:
        print(extension)

# Create, read, update and publish an extension
response = client.extensions.create(
    name='Shop', category='ecommerce', description='Shop extension',
    base_api_url='https://shop.example.com', auth_type='api_key', is_paid=False)
extensionid = response.data['extensionid']

client.extensions.get(extensionid=extensionid)
client.extensions.update(extensionid=extensionid, description='Updated')
client.extensions.publish(extensionid=extensionid, is_published=True)

# Manage the actions of an extension
response = client.extensions.list_actions(extensionid=extensionid)
response = client.extensions.create_action(
    extensionid=extensionid, name='Orders', method='GET',
    endpoint='/orders', description='List orders')
actionid = response.data['actionid']

client.extensions.get_action(extensionid=extensionid, actionid=actionid)
client.extensions.update_action(
    extensionid=extensionid, actionid=actionid, description='Updated')
client.extensions.publish_action(extensionid=extensionid, actionid=actionid)
client.extensions.delete_action(extensionid=extensionid, actionid=actionid)

# Manage pricing plans
response = client.extensions.create_pricing_plan(
    extensionid=extensionid, name='Pro', price='10000',
    billing_period='monthly', features={'orders': 100})
pricingplanid = response.data['pricingplanid']

client.extensions.update_pricing_plan(
    extensionid=extensionid, pricingplanid=pricingplanid, price='15000')
client.extensions.delete_pricing_plan(
    extensionid=extensionid, pricingplanid=pricingplanid)

# Upload a square PNG or JPEG logo
client.extensions.upload_logo(extensionid=extensionid, logo='./logo.png')
```

## <a name="log"></a> Logs Activities

```python
import logging
from nimbasms import Client

client = Client('XXXX', 'XXXX')
logging.basicConfig()  # log in console
logging.basicConfig(filename='./log.txt')  # or log in file
client.http_client.logger.setLevel(logging.INFO)
```

## Credit

Nimba SMS
