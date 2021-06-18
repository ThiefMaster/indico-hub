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
    'contact': '2067473224',
    'email': 'h.alnamer@cern.ch',
    'organization': 'it',
    'url': 'https://github.com',
}
resp = requests.post(
    BASE + 'api/instance/67c82082-b014-4097-b23e-8b04b7b57739', json=payload
)
print(resp.json())

payload = {
    'enabled': False,
}
resp = requests.post(
    BASE + 'api/instance/67c82082-b014-4097-b23e-8b04b7b57739', json=payload
)
if resp:
    print(resp.json())


# tests for GET /instance/<uuid>
resp = requests.get(BASE + 'api/instance/67c82082-b014-4097-b23e-8b04b7b57739')
if resp:
    print(resp.links)
# tests for /all
print((requests.get(BASE + 'all').json()))
