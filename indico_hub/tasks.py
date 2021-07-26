import random
from datetime import datetime

import requests


"""
This file is a script to create a inst upon call
"""


BASE = 'http://127.0.0.1:12345/'


def inst(url, contact, email, org):
    print(f'pushing {url}, {contact}, {email}, {org}')
    uuid = createInst(url, contact, email, org)
    uuid = uuid.json()['uuid']
    print(uuid)
    es_push_overhead(uuid)


def es_push_overhead(uuid):
    year = 2015
    month = 1
    day = 1
    events = 0
    contrib = 0
    users = 0
    attach = 0
    while year <= 2021:
        if month == 12:
            month = 1
            year += 1
            continue
        if day == 30:
            day = 1
            month += 1
            continue
        timestamp = str(datetime(year, month, day, 10, 10, 10))
        events += 1
        contrib += 1
        users += 1
        attach += 1
        day += 29
        pushInfo_es(uuid, events, contrib, users, attach, timestamp)


def createInst(url, contact, email, org):
    payload = {'url': url, 'contact': contact, 'email': email, 'organization': org}
    resp = requests.post(BASE + 'api/instance/', json=payload)
    return resp


def pushInfo_es(uuid, events, contributions, users, attachments, timestamp):
    events = events
    contributions = contributions
    users = users
    attachments = attachments

    payload = {
        "debug": False,
        "indico_version":"3.0",
        "language":"en_GB",
        "operating_system":"CentOS Linux 7",
        "postgres_version":"9.6.20",
        "python_version":"3.9.6",
        'events': events,
        'contributions': contributions,
        'users': users,
        'attachments': attachments,
        'timestamp': timestamp,
    }

    url = BASE + 'api' + '/instance/' + uuid + '/submit'
    print('sending request to ' + url)
    resp = requests.post(url, json=payload)
    print(resp.content)

urls=open('clean', 'r')
for x in urls:
    x = x.strip()
    inst(
        x,
        f'{random.randint(0,100), random.randint(0,100)}',
        f'{random.randint(0,100)}@{random.randint(0,100)}.{random.randint(0,100)}',
        'it',
    )
