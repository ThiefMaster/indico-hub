import requests

BASE = "http://127.0.0.1:12345/"
#tests for /instance
'''
payload = {
    'uuid' : '221',
    'enabled' : True,
    'url' : 'https://github.com',
    'contact' : '2067473224',
    'email' :'h.alnamer@cern.ch',
    'organization' : 'it',
    'crawl_date' : '2018-01-01T05:06:08',
    #crawled_data = db.Column(JSONEncodedDict)
    #geolocation = db.Column(JSONEncodedDict)
    'registration_date' :'2018-01-01T05:06:08'
    }
print("sending request to "+BASE+"instance")
resp = requests.post(BASE+"api/instance", json=payload)
print(resp.json())

payload = {
    'uuid' : '69696',
    'enabled' : True,
    'url' : 'https://github.com',
    'organization' : 'it',
    'crawl_date' : '2018-01-01T05:06:08',
    #crawled_data = db.Column(JSONEncodedDict)
    #geolocation = db.Column(JSONEncodedDict)
    'registration_date' :'2018-01-01T05:06:08'
    }
print("sending request to "+BASE+"instance")
resp = requests.post(BASE+"api/instance", json=payload)
print(resp.json())

payload = {
    'uuid' : '123214',
    'enabled' : True,
    'url' : 'https://github.com',
    'contact' : '2067473224',
    'email' :'h.alnamer@cern.ch',
    'organization' : 'it',
    'crawl_date' : '2018-01-01T05:06:08',
    #crawled_data = db.Column(JSONEncodedDict)
    #geolocation = db.Column(JSONEncodedDict)
    'registration_date' :'2018-01-01T05:06:08'
    }
print("sending request to "+BASE+"instance")
resp = requests.post(BASE+"api/instance", json=payload)
print(resp.json())

'''


#tests for /instance/<string:uuid>
payload = {
    'enabled' : False,
    'url' : 'The one and onlye',
    'contact' : 'digits',
    'organization' : 'it',
}
resp = requests.post(BASE+"api/instance/123214", json=payload)
if resp: print(resp.json())

payload = {
    'enabled' : False,

}
resp = requests.post(BASE+"api/instance/123214", json=payload)
if resp: print(resp.json())



#tests for GET /instance/<uuid>
resp = requests.get(BASE+"api/instance/1214")
if resp: print(resp.links)
#tests for /all
print((requests.get(BASE+"all").json()))


