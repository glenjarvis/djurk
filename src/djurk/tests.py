#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic unit tests for Djurk App"""

# The Django function to test settings file configurations
# (override_settings) is unfortunately only available in Django 1.4 or
# higher. At the time of this writing, Django 1.4 was still in Alpha
# stage. There is benefit in running the settings tests in Django 1.4.
# The settings specific tests will, therefore, only run in Django 1.4
# or higher and will be ignored in previous versions. A point will be
# made to run these tests against Django 1.4 before releasing, to be
# certain that this code does get exercised.

import datetime
import os
import tempfile

import boto
import django
django_version = (django.VERSION[0] * 10.0 + django.VERSION[1] * 1.0) / 10
if django_version >= 1.4:
    from django.test.utils import override_settings
from django.test import TestCase

from djurk.common import (PRODUCTION_HOST, PRODUCTION_WORKER_URL, SANDBOX_HOST,
        SANDBOX_WORKER_URL, InvalidDjurkSettings, amazon_string_to_datetime,
        get_host, get_connection, get_worker_url, is_sandbox)


# This needs @override_settings/self.settings which is only available
# in Django 1.4
if django_version >= 1.4:
    class CommonTests(TestCase):
        def setUp(self):
            self.djurk_config_filename = tempfile.mkstemp()[1]

        def tearDown(self):
            os.remove(self.djurk_config_filename)

        def test_amazon_string_to_datetime(self):
            sample_date = '2012-04-04T22:31:03Z'
            self.assertEqual(
                    amazon_string_to_datetime(sample_date),
                    datetime.datetime(2012, 4, 4, 22, 31, 3))
        #def amazon_string_to_datetime(amazon_string):
        #    amazon_iso_format = '%Y-%m-%dT%H:%M:%SZ'
        #    return datetime.datetime.strptime(
        #            amazon_string,
        #            amazon_iso_format)

        def test_get_hosts(self):
            with self.settings(DJURK={}, DJURK_CONFIG_FILE=None):
                self.assertEqual(get_host(), PRODUCTION_HOST)

            with self.settings(DJURK={'host': SANDBOX_HOST},
                               DJURK_CONFIG_FILE=None):
                self.assertEqual(get_host(), SANDBOX_HOST)

            with self.settings(DJURK={'host': PRODUCTION_HOST},
                               DJURK_CONFIG_FILE=None):
                self.assertEqual(get_host(), PRODUCTION_HOST)

            with self.settings(DJURK={
                'host': 'http://mechanicalturk.sandbox.amazonaws.com'},
                               DJURK_CONFIG_FILE=None):
                self.assertEqual(get_host(), SANDBOX_HOST)

            with self.settings(DJURK={
                'host': 'https://mechanicalturk.sandbox.amazonaws.com'},
                               DJURK_CONFIG_FILE=None):
                self.assertEqual(get_host(), SANDBOX_HOST)

            with self.settings(DJURK={
                'host': 'http://mechanicalturk.amazonaws.com'},
                               DJURK_CONFIG_FILE=None):
                self.assertEqual(get_host(), PRODUCTION_HOST)

            with self.settings(DJURK={
                'host': 'https://mechanicalturk.amazonaws.com'},
                               DJURK_CONFIG_FILE=None):
                self.assertEqual(get_host(), PRODUCTION_HOST)

            with self.settings(DJURK={},
                    DJURK_CONFIG_FILE=self.djurk_config_filename):
                # Config file is empty
                self.assertEqual(get_host(), PRODUCTION_HOST)

            with self.settings(DJURK=None,
                    DJURK_CONFIG_FILE=self.djurk_config_filename):
                f = open(self.djurk_config_filename, 'w')
                f.write("[Connection]\nhost: %s\n" % SANDBOX_HOST)
                f.close()
                self.assertEqual(get_host(), SANDBOX_HOST)

            with self.settings(DJURK=None,
                    DJURK_CONFIG_FILE=self.djurk_config_filename):
                f = open(self.djurk_config_filename, 'w')
                f.write("[Connection]\nhost: %s\n" % PRODUCTION_HOST)
                f.close()
                self.assertEqual(get_host(), PRODUCTION_HOST)

        def test_is_sandbox(self):
            "Verify the is_sandbox setting parameter works"

            with self.settings(DJURK={'host': SANDBOX_HOST}):
                self.assertTrue(is_sandbox())

            with self.settings(DJURK={'host': PRODUCTION_HOST}):
                self.assertFalse(is_sandbox())

            with self.settings(DJURK={
                'host': 'http://mechanicalturk.sandbox.amazonaws.com'},
                               DJURK_CONFIG_FILE=None):
                self.assertTrue(is_sandbox())

            with self.settings(DJURK={
                'host': 'https://mechanicalturk.sandbox.amazonaws.com'},
                               DJURK_CONFIG_FILE=None):
                self.assertTrue(is_sandbox())

            with self.settings(DJURK={
                'host': 'http://mechanicalturk.amazonaws.com'},
                               DJURK_CONFIG_FILE=None):
                self.assertFalse(is_sandbox())

            with self.settings(DJURK={
                'host': 'https://mechanicalturk.amazonaws.com'},
                               DJURK_CONFIG_FILE=None):
                self.assertFalse(is_sandbox())

        def test_get_connection(self):
            # As a full test would require a working AWS secret key,
            # only rudimentary tests are performed on this function
            with self.settings(DJURK=None, DJURK_CONFIG_FILE=None):
                self.assertRaises(InvalidDjurkSettings, get_connection)

            with self.settings(DJURK={'aws_access_key_id': '123'}):
                self.assertRaises(KeyError, get_connection)

            with self.settings(DJURK={'aws_secret_access_key': '123'}):
                self.assertRaises(KeyError, get_connection)

            with self.settings(DJURK={'aws_access_key_id': '123',
                                      'aws_secret_access_key': '456'}):
                mtc = get_connection()
                self.assertTrue(isinstance(get_connection(),
                                boto.mturk.connection.MTurkConnection))

            with self.settings(DJURK=None,
                    DJURK_CONFIG_FILE=self.djurk_config_filename):
                f = open(self.djurk_config_filename, 'w')
                f.write("[Connection]\naws_access_key_id: 123\n"
                        "aws_secret_access_key: 456\n")
                f.close()
                self.assertTrue(isinstance(get_connection(),
                                boto.mturk.connection.MTurkConnection))

        def test_get_worker_url(self):
            with self.settings(DJURK={'host': PRODUCTION_HOST},
                               DJURK_CONFIG_FILE=None):
                self.assertEqual(get_worker_url(), PRODUCTION_WORKER_URL)

            with self.settings(DJURK={'host': SANDBOX_HOST},
                               DJURK_CONFIG_FILE=None):
                self.assertEqual(get_worker_url(), SANDBOX_WORKER_URL)
                self.assertNotEqual(get_worker_url(), PRODUCTION_WORKER_URL)
