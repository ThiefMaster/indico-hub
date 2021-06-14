import requests

BASE = "http://127.0.0.1:12345/"
payload = {
        'contact': "Hassan",
        'email': "h.alnamer@cern.ch",
        'organization': "it"
    }
print("sending request to "+BASE+"api/instance/")
resp = requests.post(BASE+"api/instance", payload)
if resp : print(resp)
'''
resp = requests.post(BASE+ "instance")
if resp:
    print (resp)
'''