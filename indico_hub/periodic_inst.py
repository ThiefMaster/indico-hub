import random

import requests
from celery import Celery


"""
This file is a script to create a inst upon call
"""

app = Celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    url = f'www.{str(random.randint(0,100))}.com'
    contact = f'{random.randint(0,100)}'
    email = f'{random.randint(0,100)}@gmail.com'
    org = f'{random.randint(0, 100)}'
    sender.add_periodic_task(
        86400.0, inst.s(url, contact, email, org), name='add_every_24_hrs'
    )


BASE = 'http://127.0.0.1:12345/'


@app.task()
def inst(url, contact, email, org):
    print(f'pushing {url}, {contact}, {email}, {org}')
    uuid = createInst(url, contact, email, org)
    uuid = uuid.json()['uuid']
    pushInfo_es(uuid)


def createInst(url, contact, email, org):
    payload = {'url': url, 'contact': contact, 'email': email, 'organization': org}
    resp = requests.post(BASE + 'api/instance/', json=payload)
    return resp


def pushInfo_es(uuid):
    events = random.randint(0, 100)
    contributions = random.randint(0, 100)
    users = random.randint(0, 100)
    attachments = random.randint(0, 100)

    payload = {
        'python_version': '3.9.5',
        'indico_version': '3.0',
        'operating_system': 'ubuntu 20.4',
        'postgres_version': '1.1.6',
        'language': 'en',
        'debug': False,
        'events': events,
        'contributions': contributions,
        'users': users,
        'attachments': attachments,
    }

    url = BASE + 'api' + '/instance/' + uuid + '/submit'
    print('sending request to ' + url)
    resp = requests.post(url, json=payload)
    print(resp.content)
