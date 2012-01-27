#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import datetime

from boto.mturk.connection import MTurkConnection
from django.conf import settings


def amazon_string_to_datetime(amazon_string):
    amazon_iso_format = '%Y-%m-%dT%H:%M:%SZ'
    return datetime.datetime.strptime(
            amazon_string,
            amazon_iso_format)


class InvalidDjurkSettings(Exception):
    """Connection settings for Djurk are invalid"""
    def __init__(self, value):
        self.parameter = value

    def __unicode__(self):
        return repr(self.parameter)
    __str__ = __unicode__


def get_connection(use_sandbox=False):
    """Create connection based upon settings/configuration parameters

    The object returned from this function is a Mechanical Turk
    connection object. If the Mechanical Turk Connection object could
    not be created, an InvalidDjurkSettings exception is raised.

    The Django settings file should have either the DJURK or
    DJURK_CONFIG_FILE parameters defined. If both are defined, the
    DJURK parameter takes precedent. However, we encourage the use of
    the DJURK_CONFIG_FILE parameter instead -- as the settings.py file
    is often checked into a repository.  The connection parameters used
    by Djurk, especially the 'aws_secret_access_key' parameter, should
    be kept private. Thus, the DJURK_CONFIG_FILE parameter indicates a
    file that will not be checked into a repository. Care should be
    taken that this file is not readable by other users/processes on
    the system.

    If the DJURK parameter is used in the settings file, it will have a
    syntax similar to the following:

    DJURK = {
        'aws_access_key_id': 'BJLBD8MOPC4ZDEB37QFB',
        'aws_secret_access_key': 'g8Xw/sCOLY5WYtS091kcVdy0cMUZgdSdS',
        'host': 'mechanicalturk.amazonaws.com',
        'debug': 1
    }

    The host and debug parameters are optional and, if omitted,
    defaults are used. The host is the Amazon Mechanical Turk host with
    which to connect.  If the use_sandbox boolean argument passed to
    this function is True, the sandbox host
    'mechanicalturk.sandbox.amazonaws.com' is used instead (regardless
    what configuration/setting parameter is set.  Debug is the
    level of debug information printed by the boto library.

    If the DJURK_CONFIG_FILE Django settings parameter is used, it
    should point to a file name that is parsable by ConfigParser. An
    example of these contents follow:

    [Connection]
    aws_access_key_id: 'BJLBD8MOPC4ZDEB37QFB'
    aws_secret_access_key: 'g8Xw/sCOLY5WYtS091kcVdy0cMUZgdSdS'
    host: 'mechanicalturk.amazonaws.com'
    debug: 1
    """
    PRODUCTION_HOST = 'mechanicalturk.amazonaws.com'
    SANDBOX_HOST = 'mechanicalturk.sandbox.amazonaws.com'

    host = PRODUCTION_HOST
    debug = 1

    if hasattr(settings, 'DJURK'):
        aws_access_key_id = settings.DJURK['aws_access_key_id']
        aws_secret_access_key = settings.DJURK['aws_secret_access_key']
        if 'host' in settings.DJURK:
            host = settings.DJURK['host']
        if 'debug' in settings.DJURK:
            debug = settings.DJURKp['debug']
    elif hasattr(settings, 'DJURK_CONFIG_FILE'):
        config = ConfigParser.ConfigParser()
        config.read(settings.DJURK_CONFIG_FILE)

        aws_access_key_id = config.get('Connection',
                                       'aws_access_key_id')
        aws_secret_access_key = config.get('Connection',
                                           'aws_secret_access_key')
        if config.has_option('Connection', 'host'):
            host = config.get('Connection', 'host')
        if config.has_option('Connection', 'debug'):
            debug = config.get('Connection', 'debug')
    else:
        raise InvalidDjurkSettings("Djurk settings not found")

    if use_sandbox:
        host = SANDBOX_HOST

    return MTurkConnection(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        host=host,
        debug=debug)
