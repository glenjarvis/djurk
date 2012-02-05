#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import datetime

from boto.mturk.connection import MTurkConnection
from django.conf import settings


PRODUCTION_HOST = u'mechanicalturk.amazonaws.com'
PRODUCTION_WORKER_URL = u'https://www.mturk.com'
SANDBOX_HOST = u'mechanicalturk.sandbox.amazonaws.com'
SANDBOX_WORKER_URL = u'https://workersandbox.mturk.com'


class InvalidDjurkSettings(Exception):
    """Connection settings for Djurk are invalid"""
    def __init__(self, value):
        self.parameter = value

    def __unicode__(self):
        return repr(self.parameter)
    __str__ = __unicode__


def amazon_string_to_datetime(amazon_string):
    """Return datetime from passed Amazon format datestring"""

    amazon_iso_format = '%Y-%m-%dT%H:%M:%SZ'
    return datetime.datetime.strptime(
            amazon_string,
            amazon_iso_format)


def get_host():
    """Read configuration file and get proper host

    The host returned will be the contents of either PRODUCTION_HOST or
    PRODUCTION_HOST as defined in this module. Because the host
    parameter is optional, if it is omitted, the PRODUCTION_HOST is
    returned. Therefore, to use the sandbox, one has to explicitly set
    the host parameter to 'mechanicalturk.sandbox.amazonaws.com' in
    either the DJURK or DJURK_CONFIG_FILE parmeters/files.
    """
    host = PRODUCTION_HOST
    if hasattr(settings, 'DJURK') and settings.DJURK is not None:
        if 'host' in settings.DJURK:
            host = settings.DJURK['host']
    elif hasattr(settings, 'DJURK_CONFIG_FILE') and\
                          settings.DJURK_CONFIG_FILE is not None:
        config = ConfigParser.ConfigParser()
        config.read(settings.DJURK_CONFIG_FILE)
        if config.has_option('Connection', 'host'):
            host = config.get('Connection', 'host')

    if host.startswith('http://'):
        host = host.replace('http://', '', 1)

    if host.startswith('https://'):
        host = host.replace('https://', '', 1)

    assert host in [SANDBOX_HOST, PRODUCTION_HOST]

    return host


def is_sandbox():
    """Return True if configuration is configured to connect to sandbox"""

    host = get_host()
    return host == SANDBOX_HOST


def get_worker_url():
    """Get proper URL depending upon sandbox settings"""

    if is_sandbox():
        return SANDBOX_WORKER_URL
    else:
        return PRODUCTION_WORKER_URL


def get_connection():
    """Create connection based upon settings/configuration parameters

    The object returned from this function is a Mechanical Turk
    connection object. If the Mechanical Turk Connection object could
    not be created, an InvalidDjurkSettings exception is raised.

    The Django settings file should have either the DJURK or
    DJURK_CONFIG_FILE parameters defined (and not set to None). If both
    are defined (and not None), the DJURK parameter takes precedent.
    However, we encourage the use of the DJURK_CONFIG_FILE parameter
    instead -- as the settings.py file is often checked into a
    repository.  The connection parameters used by Djurk, especially
    the 'aws_secret_access_key' parameter, should be kept private.
    Thus, the DJURK_CONFIG_FILE parameter indicates a file that should
    not be checked into a repository. Care should be taken that this
    file is not readable by other users/processes on the system.

    If the DJURK parameter is used in the settings file, it will have a
    syntax similar to the following:

    DJURK = {
        'aws_access_key_id': 'BJLBD8MOPC4ZDEB37QFB',
        'aws_secret_access_key': 'g8Xw/sCOLY5WYtS091kcVdy0cMUZgdSdS',
        'host': 'mechanicalturk.sandbox.amazonaws.com',
        'debug': 1
    }

    The host and debug parameters are optional and, if omitted,
    defaults are used. The host is the Amazon Mechanical Turk host with
    which to connect. There are two choices, production or sandbox. If
    omitted, production is used.  Debug is the level of debug
    information printed by the boto library.

    If the DJURK_CONFIG_FILE Django settings parameter is used, it
    should point to a file name that is parsable by ConfigParser. An
    example of these contents follow:

    [Connection]
    aws_access_key_id: 'BJLBD8MOPC4ZDEB37QFB'
    aws_secret_access_key: 'g8Xw/sCOLY5WYtS091kcVdy0cMUZgdSdS'
    host: 'mechanicalturk.amazonaws.com'
    debug: 1
    """

    host = get_host()
    debug = 1

    if hasattr(settings, 'DJURK') and settings.DJURK is not None:
        aws_access_key_id = settings.DJURK['aws_access_key_id']
        aws_secret_access_key = settings.DJURK['aws_secret_access_key']
        if 'debug' in settings.DJURK:
            debug = settings.DJURK['debug']
    elif hasattr(settings, 'DJURK_CONFIG_FILE') and\
                          settings.DJURK_CONFIG_FILE is not None:
        config = ConfigParser.ConfigParser()
        config.read(settings.DJURK_CONFIG_FILE)

        aws_access_key_id = config.get('Connection',
                                       'aws_access_key_id')
        aws_secret_access_key = config.get('Connection',
                                           'aws_secret_access_key')
        if config.has_option('Connection', 'debug'):
            debug = config.get('Connection', 'debug')
    else:
        raise InvalidDjurkSettings("Djurk settings not found")

    return MTurkConnection(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        host=host,
        debug=debug)
