#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import messages

from djurk.models import Assignment, HIT, KeyValue
from djurk.helpers import update_all_hits, update_reviewable_hits


def dispose_hit(modeladmin, request, queryset):
    for hit in queryset:
        hit.dispose()
        messages.info(request, "Disposed data for %s." % hit)
dispose_hit.short_description = "Dispose of HIT data from Mechanical Turk"


def expire_hit(modeladmin, request, queryset):
    for hit in queryset:
        hit.expire()
        messages.info(request, "Expired %s." % hit)
expire_hit.short_description = "Expire HIT on Mechanical Turk"


def poll_all_hits(modeladmin, request, queryset):
    update_all_hits()
    messages.info(request, "Poll all HITs finished.")
poll_all_hits.short_description = "Poll all HITs from Mechanical Turk"


def poll_reviewable_hits(modeladmin, request, queryset):
    update_reviewable_hits()
    messages.info(request, "Poll reviewable HITs finished.")
poll_reviewable_hits.short_description = "Poll reviewable HITs from MTurk"


def update_hit(modeladmin, request, queryset):
    for hit in queryset:
        hit.update(do_update_assignments=True)
        messages.info(request, "Updated %s." % hit)
update_hit.short_description = "Update this HIT from Mechanical Turk"


def approve_assignment(modeladmin, request, queryset):
    for assignment in queryset:
        assignment.approve()
        messages.info(request, "Approved %s." % assignment)
approve_assignment.short_description = "Approve assignment and pay worker"


def reject_assignment(modeladmin, request, queryset):
    for assignment in queryset:
        assignment.reject()
        messages.info(request, "Rejected %s." % assignment)
reject_assignment.short_description = "Reject assignment (Don't pay worker)"


class KeyValueInline(admin.TabularInline):
    model = KeyValue
    readonly_fields = ('key', 'value')


class HIT_Admin(admin.ModelAdmin):
    actions = [dispose_hit, expire_hit, poll_all_hits, poll_reviewable_hits,
               update_hit]
    date_hierarchy = 'creation_time'
    fieldsets = (

            (None, {
                'fields': (('mturk_id', 'hit_type_id'),
                           ('creation_time', 'status'),
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
                     'review_status',
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
            ('Attached Objects', {
                'classes': ('collapse',),
                'fields': (
                     'content_type',
                     'content_id',
                 )
            }),
    )
    list_display = (
        'creation_time',
        'status',
        'mturk_id',
        'hit_type_id',
        'title',
        'reward'
    )
    readonly_fields = (
        'mturk_id',
        'hit_type_id',
        'creation_time',
        'status',
        'review_status',
        'title',
        'keywords',
        'description',
        'reward',
        'lifetime_in_seconds',
        'auto_approval_delay_in_seconds',
        'number_of_similar_hits',
        'review_status',
        'max_assignments',
        'assignment_duration_in_seconds',
        'number_of_assignments_pending',
        'number_of_assignments_available',
        'number_of_assignments_completed',
    )
    list_display_links = list_display
    list_filter = (
        'status',
        'review_status',
        'creation_time',
    )
    read_only_fields = ('creation_time',)
    search_fields = (
        'mturk_id',
        'hit_type_id',
        'title',
        'description',
        'keywords',
    )


class AssignmentAdmin(admin.ModelAdmin):
    actions = [approve_assignment, reject_assignment, update_hit]
    search_fields = ('mturk_id',)
    date_hierarchy = 'submit_time'
    list_display = (
        'mturk_id',
        'auto_approval_time',
        'worker_id',
        'hit',
        'status',
    )
    list_filter = (
        'status',
    )
    fieldsets = (
            (None, {
                'fields': (('mturk_id', 'worker_id',),
                           ('hit', 'status'),
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
    readonly_fields = ('mturk_id', 'hit',
                       'worker_id', 'status')
    inlines = [
        KeyValueInline,
    ]


class KeyValueAdmin(admin.ModelAdmin):
    list_display = (
        'assignment',
        'key',
        'short_value',
    )

admin.site.register(HIT, HIT_Admin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(KeyValue, KeyValueAdmin)
