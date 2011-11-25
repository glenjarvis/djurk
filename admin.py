#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from djurk.models import HIT

class HIT_Admin(admin.ModelAdmin):
    list_display = (
        'creation_time',
        'hit_id',
        'hit_type_id',
        'title',
        'reward'
    )
    list_filter = (
        'creation_time',
        'hit_status',
        'hit_review_status',
    )
    search_fields = (
        'hit_id',
        'hit_type_id',
        'title',
        'description',
        'keyword',
    )

admin.site.register(HIT, HIT_Admin)
