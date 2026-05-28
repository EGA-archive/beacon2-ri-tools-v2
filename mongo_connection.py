from urllib.parse import quote_plus
import os

from pymongo.mongo_client import MongoClient

import conf.conf as conf


def _get_config_value(name, default=''):
    env_value = os.getenv(name.upper())
    if env_value is None:
        env_value = os.getenv(name)
    if env_value not in (None, ''):
        return env_value
    return getattr(conf, name, default)


def build_mongo_uri():
    uri = _get_config_value('database_uri')
    if uri:
        return uri

    uri = _get_config_value('mongodb_uri')
    if uri:
        return uri

    host = _get_config_value('database_host', 'mongo')
    if host.startswith(('mongodb://', 'mongodb+srv://')):
        return host

    user = _get_config_value('database_user', '')
    password = _get_config_value('database_password', '')
    database_name = _get_config_value('database_name', 'beacon')
    auth_source = _get_config_value('database_auth_source', 'admin')
    port = _get_config_value('database_port', 27017)

    credentials = ''
    if user or password:
        credentials = '{}:{}@'.format(
            quote_plus(str(user)),
            quote_plus(str(password)),
        )

    uri = 'mongodb://{}{}:{}/{}'.format(
        credentials,
        host,
        port,
        database_name,
    )

    if auth_source:
        uri += '?authSource={}'.format(quote_plus(str(auth_source)))

    return uri


def build_mongo_client():
    return MongoClient(build_mongo_uri())


def build_mongo_database():
    database_name = _get_config_value('database_name', 'beacon')
    return build_mongo_client()[database_name]
