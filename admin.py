#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from djurk.models import Assignment, HIT, KeyValue


class HIT_Admin(admin.ModelAdmin):
    date_hierarchy = 'creation_time'
    fieldsets = (
            (None, {
                'fields': (('hit_id', 'hit_type_id'),
                           ('creation_time', 'hit_status'),
                           ('title', 'keywords', 'description'),
                           'reward',
                           'requester_annotation',
                           ),
            }),
            ('HIT Details', {
                'classes': ('collapse',),
                'fields': (
                     'lifetime_in_seconds',
                     'auto_approval_delay_in_seconds',
                     'number_of_similar_hits',
                     'hit_review_status',
                 )
            }),
            ('Assignment Overview', {
                'classes': ('collapse',),
                'fields': (
                     'max_assignments',
                     'assignment_duration_in_seconds',
                     'number_of_assignments_pending',
                     'number_of_assignments_available',
                     'number_of_assignments_completed',
                 )
            }),
    )
    list_display = (
        'creation_time',
        'hit_id',
        'hit_type_id',
        'title',
        'reward'
    )
    readonly_fields = (
        'creation_time',
        'hit_id',
        'hit_type_id',
        'hit_status',
        'hit_review_status',
    )
    list_display_links = list_display
    list_filter = (
        'hit_status',
        'hit_review_status',
        'creation_time',
    )
    read_only_fields = ('creation_time',)
    search_fields = (
        'hit_id',
        'hit_type_id',
        'title',
        'description',
        'keyword',
    )

class AssignmentAdmin(admin.ModelAdmin):
    date_hierarchy = 'submit_time'
    list_display = (
        'assignment_id',
        'auto_approval_time',
        'worker_id',
        'hit',
        'assignment_status',
    )
    list_filter = (
        'assignment_status',
    )
    fieldsets = (
            (None, {
                'fields': (('assignment_id', 'worker_id',),
                           'hit',
                           'requester_feedback',
                           ),
            }),
            ('Times', {
                'classes': ('collapse',),
                'fields': ('submit_time',
                           'approval_time',
                           'auto_approval_time',
                           'accept_time',
                           'rejection_time',
                           'deadline',
                           ),
            }),
    )
    readonly_fields = ('assignment_id', 'hit',
                       'worker_id',)

class KeyValueAdmin(admin.ModelAdmin):
    list_display = (
        'assignment',
        'key',
        'short_value',
    )

admin.site.register(HIT, HIT_Admin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(KeyValue, KeyValueAdmin)
