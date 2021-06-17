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
resp = requests.post(BASE + 'api/instance', json=payload)
print(resp.json())

payload = {
    'url': 'https://github.com',
    'organization': 'it',
}
print('sending request to ' + BASE + 'instance')
resp = requests.post(BASE + 'api/instance', json=payload)
print(resp.json())

payload = {
    'url': 'https://github.com',
    'contact': '2067473224',
    'email': 'h.alnamer@cern.ch',
    'organization': 'it',
}
print('sending request to ' + BASE + 'instance')
resp = requests.post(BASE + 'api/instance', json=payload)
print(resp.json())


# tests for /instance/<string:uuid>
payload = {
    'enabled': False,
    'url': 'The one and onlye',
    'contact': 'digits',
    'organization': 'it',
}
resp = requests.post(BASE + 'api/instance/123214', json=payload)
if resp:
    print(resp.json())

payload = {
    'enabled': False,
}
resp = requests.post(BASE + 'api/instance/123214', json=payload)
if resp:
    print(resp.json())


# tests for GET /instance/<uuid>
resp = requests.get(BASE + 'api/instance/1214')
if resp:
    print(resp.links)
# tests for /all
print((requests.get(BASE + 'all').json()))
