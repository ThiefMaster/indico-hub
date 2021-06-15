import requests

BASE = "http://127.0.0.1:12345/"
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

print("sending request to "+BASE+"api/instance")
resp = requests.post(BASE+"api/instance", payload)
if resp : print(resp.json())
'''
resp = requests.post(BASE+ "instance")
if resp:
    print (resp)
'''