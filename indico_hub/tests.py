import json

import requests


BASE = 'http://127.0.0.1:12345/'
# tests for /instance

payload = {
    'url': 'https://github.com',
    'contact': '2067473224',
    'email': 'h.alnamer@cern.ch',
    'organization': 'it',
}
print('sending request to ' + BASE + 'instance')
resp = requests.post(BASE + 'api/instance/', json=payload)
print(resp)

payload = {
    'url': 'https://github.com',
    'organization': 'it',
}
print('sending request to ' + BASE + 'instance')
resp = requests.post(BASE + 'api/instance/', json=payload)
print(resp.json())

payload = {
    'url': 'https://github.com',
    'contact': '2067473224',
    'email': 'h.alnamer@cern.ch',
    'organization': 'it',
}
print('sending request to ' + BASE + 'instance')
resp = requests.post(BASE + 'api/instance/', json=payload)
print(resp.json())


# tests for /instance/<string:uuid>
"""
prepping data for tests
"""
resp = requests.get(BASE + 'all')
all = json.loads(resp.content)
payload = {
    'contact': '2067473224',
    'email': 'h.alnamer@cern.ch',
    'organization': 'it',
    'url': 'https://github.com',
}
resp = requests.post(BASE + 'api/instance/' + str(all.pop()['uuid']), json=payload)
print(resp.json())

payload = {
    'enabled': False,
}
resp = requests.post(BASE + 'api/instance/' + str(all.pop()['uuid']), json=payload)
if resp:
    print(resp.json())


# tests for GET /instance/<uuid>
resp = requests.get(BASE + 'api/instance/' + str(all.pop()['uuid']))
if resp:
    print(resp.links)
# tests for /all
print((requests.get(BASE + 'all').json()))


def infoCelery():
    payload = {
        'python_version': '3.9.5',
        'indico_version': '3.0',
        'operating_system': 'ubuntu 20',
        'postgres_version': '1.1.6',
        'language': 'en',
        'debug': False,
    }
    resp = requests.post(
        BASE + 'api/instance/' + str(all.pop()['uuid']), json=payload
    )
    print(resp.content)
