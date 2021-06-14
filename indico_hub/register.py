import requests
import json
import requests
from requests.exceptions import HTTPError, RequestException, Timeout
from werkzeug.urls import url_join
COMMUNITY_HUB_URL = "https://hub.getindico.io"
BASE_URL = None
DEBUG= False
HEADERS = {'Content-Type': 'application/json'}
TIMEOUT = 10

def _get_url():
    return url_join(COMMUNITY_HUB_URL, 'api/instance/')


'''
This is a handmade about working request to the 
server 
could be buggy!
'''
def register(contact, email):
    payload = {
        'url': BASE_URL,
        'contact': contact,
        'email': email,
        'organization': "it"
    }
    response = requests.post(_get_url(), 
        data=json.dumps(payload), headers=HEADERS, 
        timeout=TIMEOUT,
        verify=(not DEBUG))
    try:
        response.raise_for_status()
    except HTTPError as err:
        msg = 'failed to register the server to the community hub, got: '+ str(err)
        return msg
        
    except Timeout:
        msg = 'failed to register: timeout while contacting the community hub'
        return msg
        
    except RequestException as err:
        msg = "unexpected exception while registering the server with the Community Hub: " + str(err)
        return msg
        

    json_response = response.json()
    if 'uuid' not in json_response:
        logger.error('invalid json reply from the community hub: uuid missing')
        cephalopod_settings.set('joined', False)
        raise ValueError('invalid json reply from the community hub: uuid missing')

    cephalopod_settings.set_multi({
        'joined': True,
        'uuid': json_response['uuid'],
        'contact_name': payload['contact'],
        'contact_email': payload['email']
    })
    msg = 'successfully registered the server to the community hub'
    return msg


