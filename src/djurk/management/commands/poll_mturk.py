#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Cron job to constantly poll Amazon Mechanical Turk"""

import logging
import time
from optparse import make_option

from django.core.management.base import BaseCommand

from djurk.common import get_connection
from djurk.helpers import update_all_hits, update_reviewable_hits

SLEEP_TIME = 5 * 60  # 5 minutes


class NullHandler(logging.Handler):
    """Create silent logger to avoid confusion for new programmers

    If logging is needed, it can be passed into this cronjob. However,
    if logging isn't provided, a message such as "No handlers could be
    found for logger..." is often printed. This adds confusion.

    This is avoided by defining this handler that does not log. A
    logging handler can be substituted instead if the output is
    needed.
    """
    def emit(self, record):
        pass

logger = logging.getLogger("djurk").addHandler(NullHandler())


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--assignments',
            action='store_true',
            dest='do_update_assignments',
            default=False,
            help='Update Assignments as well as HITs (more intensive)'),
        make_option(
            '--reviewable',
            action='store_true',
            dest='reviewable',
            default=False,
            help=('Only update reviewable HITs (less demand on MTurk - '
                  ' possibly miss HITs)')),
        make_option(
            '--loop',
            action='store_true',
            dest='loop',
            default=False,
            help='Use Amazon Mechanical Turk Sandbox (instead of production)'),
    )

    def handle(self, *args, **options):
        mtc = get_connection()
        do_update_assignments = options['do_update_assignments']

        while True:
            if options['reviewable']:
                logging.info(("Updating Reviewable HITs with "
                              "Assignments: %s") % do_update_assignments)
                update_reviewable_hits(
                        do_update_assignments=do_update_assignments)
            else:
                logging.info(("Updating All HITs with "
                              "Assignments: %s") % do_update_assignments)
                update_all_hits(
                        do_update_assignments=do_update_assignments)
            logging.info("Sleeping")
            if not options['loop']:
                break
            time.sleep(SLEEP_TIME)
