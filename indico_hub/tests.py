import json

import requests


BASE = 'http://127.0.0.1:12345/'
resp = requests.get(BASE + 'all')
all = json.loads(resp.content)
# tests for /instance

def reg1():
    payload = {
        'url': 'https://github.com',
        'contact': '2067473224',
        'email': 'h.alnamer@cern.ch',
        'organization': 'it',
    }
    print('sending request to ' + BASE + 'instance')
    resp = requests.post(BASE + 'api/instance/', json=payload)
    print(resp)
def reg2():
    payload = {
        'url': 'https://github.com',
        'organization': 'it',
    }
    print('sending request to ' + BASE + 'instance')
    resp = requests.post(BASE + 'api/instance/', json=payload)
    print(resp.json())

def reg3():
    payload = {
        'url': 'https://github.com',
        'contact': '2067473224',
        'email': 'h.alnamer@cern.ch',
        'organization': 'it',
    }
    print('sending request to ' + BASE + 'instance')
    resp = requests.post(BASE + 'api/instance/', json=payload)
    print(resp.json())


# tests for /instance/<string:uuid>::update the instance data
"""
prepping data for tests
"""
def update1():
    payload = {
        'contact': '2067473224',
        'email': 'h.alnamer@cern.ch',
        'organization': 'it',
        'url': 'https://github.com',
    }
    resp = requests.post(BASE + 'api/instance/' + str(all.pop()['uuid']), json=payload)
    print(resp.content))

def update2():
    payload = {
        'enabled': False,
    }
    resp = requests.post(BASE + 'api/instance/' + str(all.pop()['uuid']), json=payload)
    print(resp.content)


# tests for GET /instance/<uuid>
def get1():
    resp = requests.get(BASE + 'api/instance/' + str(all.pop()['uuid']))
    print(resp.content)
# tests for /all
def getAll():
    print((requests.get(BASE + 'all').json()))


def post_es():
    payload = {
        'python_version': 'https://github.com',
        'indico_version': '2067473224',
        'operating_system': 'h.alnamer@cern.ch',
        'postgres_version': 'it',
        'language': 'en',
        'debug': False,
    }
    uuid = '/' + all.pop()['uuid']
    print(str(uuid))

    url = BASE + 'api' + '/instance' + uuid + '/submit'
    print('sending request to ' + url)
    resp = requests.post(url, json=payload)
    print(resp.content)

def get_es():
    uuid = '/' + all.pop()['uuid']
    url = BASE + 'api' + '/instance' + uuid + '/get'
    resp = requests.get(url)
    print(resp.content)
