import socket
from urllib.parse import urlparse

from .db import db
from .es_conf import es, index_name


def geolocate(instance):
    url = urlparse(instance.url).hostname

    try:
        ip_address = socket.gethostbyname(url)
    except socket.gaierror:
        return

    new_doc = es.get(index=index_name, id=instance.uuid)['_source']
    new_doc['ip'] = ip_address
    es.index(index=index_name, id=instance.uuid, body=new_doc, pipeline='geoip')
    doc = es.get(index=index_name, id=instance.uuid)['_source']
    instance.geolocation = doc['geoip']
    db.session.commit()
    return f"reside at {doc['geoip']['continent_name']}"
