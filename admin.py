#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from djurk.models import Assignment, HIT


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
        'worker_id',
        'hit',
        'assignment_status',
    )

# auto_approval_time = models.DateTimeField(
# accept_time = models.DateTimeField(
# submit_time = models.DateTimeField(
# approval_time = mod
# rejection_time = models.DateTimeField(
# deadline = models.DateTimeField(
# requester_feedback = 

admin.site.register(HIT, HIT_Admin)
admin.site.register(Assignment, AssignmentAdmin)
