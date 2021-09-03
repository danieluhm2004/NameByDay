import os
import json
from datetime import datetime
from pyicloud import PyiCloudService

today = datetime.today()
email = os.environ.get('NBD_ICLOUD_EMAIL')
password = os.environ.get('NBD_ICLOUD_PASSWORD')
phone_number = os.environ.get('NBD_PHONE_NUMBER')
dday_date = os.environ.get('NBD_DDAY_DATE')

name_prefix = os.environ.get('NBD_NAME_PREFIX', "")
name_suffix = os.environ.get('NBD_NAME_SUFFIX', "")
name_sunday = os.environ.get('NBD_NAME_SUNDAY', '🤍')
name_monday = os.environ.get('NBD_NAME_MONDAY', '❤️')
name_tuesday = os.environ.get('NBD_NAME_TUESDAY', '🧡')
name_wednesday = os.environ.get('NBD_NAME_WEDNESDAY', '💛')
name_thursday = os.environ.get('NBD_NAME_THURSDAY', '💚')
name_friday = os.environ.get('NBD_NAME_FRIDAY', '💙')
name_saturday = os.environ.get('NBD_NAME_SATURDAY', '💜')

if email is None or password is None or phone_number is None:
    print("NBD_ICLOUD_EMAIL and NBD_ICLOUD_PASSWORD and NBD_ICLOUD_PHONE_NUMBER environment are required.")
    exit(1)

icloud = PyiCloudService(email, password, 'sessions')
refresh_params = None
refresh_response = None
contacts_params = None
contacts_response = None
update_params = None
update_response = None

if icloud.requires_2fa:
    print('Two-factor authentication required.')
    code = input(
        "Enter the code you received of one of your approved devices: ")
    result = icloud.validate_2fa_code(code)
    print("Code validation result: %s" % result)

    if not result:
        print("Failed to verify security code")
        exit(1)

    if not icloud.is_trusted_session:
        print("Session is not trusted. Requesting trust...")
        result = icloud.trust_session()
        print("Session trust result %s" % result)

        if not result:
            print(
                "Failed to request trust. You will likely be prompted for the code again in the coming weeks")

if icloud.requires_2sa:
    import click
    print("Two-step authentication required. Your trusted devices are:")

    devices = icloud.trusted_devices
    for i, device in enumerate(devices):
        print("  %s: %s" % (i, device['deviceName'],
                            "SMS to %s" % device.get('phoneNumber')))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not icloud.send_verification_code(device):
        print("Failed to send verification code")
        exit(1)

    code = click.prompt('Please enter validation code')
    if not icloud.validate_verification_code(device, code):
        print("Failed to verify verification code")
        exit(1)


def refresh_contacts(self):
    global refresh_params, refresh_response

    refresh_params = dict(self.params)
    refresh_params.update(
        {"clientVersion": "2.1", "locale": "en_US", "order": "last,first", }
    )

    req = self.session.get(self._contacts_refresh_url, params=refresh_params)
    refresh_response = req.json()

    return refresh_response


def get_all_contacts(self):
    global contacts_params, contacts_response

    contacts_params = dict(refresh_params)
    contacts_params.update({
        "prefToken": refresh_response["prefToken"],
        "syncToken": refresh_response["syncToken"],
        "limit": "0",
        "offset": "0",
    })

    req = self.session.get(self._contacts_next_url, params=contacts_params)
    contacts_response = req.json()
    return contacts_response["contacts"]


def update_contacts(self, contact):
    global update_params, update_response
    contacts_modify_url = "%s/contacts/card" % self._contacts_endpoint
    del contact['normalized']
    body = json.dumps({"contacts": [contact]})
    update_params = dict(contacts_params)
    update_params.update({"method": "PUT"})
    req = self.session.post(contacts_modify_url,
                            params=update_params,
                            data=body)
    update_response = req.json()
    return update_response["contacts"]


def get_contact_by_phone(contacts, phone: str):
    for contact in contacts:
        if 'phones' not in contact:
            continue
        phones = contact['phones']
        if(phones != None and len(phones) > 0 and phones[0]['field'] == phone):
            return contact
    return None


def get_today_name() -> str:
    if(datetime.today().weekday() == 0):
        return name_monday
    if(datetime.today().weekday() == 1):
        return name_tuesday
    if(datetime.today().weekday() == 2):
        return name_wednesday
    if(datetime.today().weekday() == 3):
        return name_thursday
    if(datetime.today().weekday() == 4):
        return name_friday
    if(datetime.today().weekday() == 5):
        return name_saturday
    if(datetime.today().weekday() == 6):
        return name_sunday


def get_dday() -> int:
    target = datetime.strptime(dday_date, '%Y-%m-%d')
    return (today - target).days


refresh_contacts(icloud.contacts)
contacts = get_all_contacts(icloud.contacts)
contact = get_contact_by_phone(contacts, phone_number)
if contact == None:
    print('Cannot find contact by phone number')
    exit(1)

name = name_prefix
if dday_date != None:
    name += "%s" % get_dday()
name += name_suffix
name += get_today_name()

if(contact['firstName'] == name):
    print('Contact name is already %s' % name)
    exit(0)

contact['lastName'] = ""
contact['firstName'] = name
update_contacts(icloud.contacts, contact)
