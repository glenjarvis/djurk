#!/usr/bin/env python
# -*- coding: utf-8 -*-

from djurk.common import get_connection
from djurk.models import HIT


def _update_hits(iterable):
    for mturk_hit in iterable:
        djurk_hit = HIT.objects.get_or_create(mturk_id=mturk_hit.HITId)[0]
        djurk_hit.update(mturk_hit=mturk_hit)


def update_all_hits():
    """Get All HITS from Amazon"""
    connection = get_connection()
    _update_hits(connection.get_all_hits())


def update_reviewable_hits():
    """Get only reviewable HITS from Amazon"""
    connection = get_connection()
    _update_hits(connection.get_reviewable_hits())
