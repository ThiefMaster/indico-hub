from elasticsearch import Elasticsearch

from .config import ELASTICSEARCH_URL


def connect_elasticsearch(**kwargs):
    _es_config = ELASTICSEARCH_URL
    _es_hosts = [_es_config]
    if 'hosts' in kwargs.keys():
        _es_hosts = kwargs['hosts']
    _es_obj = None
    _es_obj = Elasticsearch(hosts=_es_hosts, timeout=10)
    if _es_obj.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es_obj


es = connect_elasticsearch()
