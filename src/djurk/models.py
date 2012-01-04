#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Amazon Mechanical Turk Data Structures implemented as Django models

The Human Intelligent Task (HIT) related data that is created by using
Amazon Mechanical Turk can be transient. After the data is retrieved
from Mechanial Turk, it is often stored locally. These Django models
mimic the Amazon Mechanical Turk data structures as specified in the
"Amazon Mechanical Turk API Reference (API Version 2008-08-02):

http://docs.amazonwebservices.com/AWSMechTurk/2008-08-02/AWSMturkAPI/

To keep the experience easier for a Django user, Python and Django
conventions are used whenever possible. For example, the Mechanical Turk
API has an attribute 'HITTypeId.' However, when modeled here, that
attribute has name 'hit_type_id.' An exception to that rule is that many
string based fields in the Mechanical Turk API return Null/None. Django
prefers not to allow CharFields to be nullable as both Null/None and the
empty string are redundant. As the API does return nullable data types,
we broke with Django convention on that point.
"""

import boto
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_init

from djurk.common import amazon_string_to_datetime, get_connection


def init_connection_callback(sender, **signal_args):
    """Mechanical Turk connection signal callback

    By using Django pre-init signals, class level connections can be
    made available to Django models that configure this pre-init
    signal.

    WARNING: Since self.connection is configured on the class level,
    any changes (e.g., to change use_sandbox=True|False) happen at the
    class level, and thus, would affect *all* connections -- not just
    newly created classes.
    """
    use_sandbox = False
    sender.args = sender
    object_args = signal_args['kwargs']
    if 'use_sandbox' in object_args:
        use_sandbox = object_args.pop(u'use_sandbox')
    sender.connection = get_connection(use_sandbox=use_sandbox)


class DisposeException(Exception):
    """Unable to Dispose of HIT Exception"""
    def __init__(self, value):
        self.parameter = value

    def __unicode__(self):
        return repr(self.parameter)
    __str__ = __unicode__


class HIT(models.Model):
    """An Amazon Mechanical Turk Human Intelligence Task as a Django Model"""

    (ASSIGNABLE, UNASSIGNABLE, REVIEWABLE, REVIEWING, DISPOSED) = (
          'A', 'U', 'R', 'G', 'D')

    (_ASSIGNABLE, _UNASSIGNABLE, _REVIEWABLE, _REVIEWING, _DISPOSED) = (
          "Assignable", "Unassignable", "Reviewable", "Reviewing", "Disposed")

    (NOT_REVIEWED, MARKED_FOR_REVIEW, REVIEWED_APPROPRIATE,
          REVIEWED_INAPPROPRIATE) = ("N", "M", "R", "I")

    (_NOT_REVIEWED, _MARKED_FOR_REVIEW, _REVIEWED_APPROPRIATE,
          _REVIEWED_INAPPROPRIATE) = ("NotReviewed", "MarkedForReview",
          "ReviewedAppropriate", "ReviewedInappropriate")

    STATUS_CHOICES = (
            (ASSIGNABLE, _ASSIGNABLE),
            (UNASSIGNABLE, _UNASSIGNABLE),
            (REVIEWABLE, _REVIEWABLE),
            (REVIEWING, _REVIEWING),
            (DISPOSED, _DISPOSED),
    )
    REVIEW_CHOICES = (
            (NOT_REVIEWED, _NOT_REVIEWED),
            (MARKED_FOR_REVIEW, _MARKED_FOR_REVIEW),
            (REVIEWED_APPROPRIATE, _REVIEWED_APPROPRIATE),
            (REVIEWED_INAPPROPRIATE, _REVIEWED_INAPPROPRIATE)
    )
    # Convenience lookup dictionaries for the above lists
    reverse_status_lookup = dict((v, k) for k, v in STATUS_CHOICES)
    reverse_review_lookup = dict((v, k) for k, v in REVIEW_CHOICES)

    mturk_id = models.CharField(
            "HIT ID",
            max_length=255,
            unique=True,
            null=True,
            help_text="A unique identifier for the HIT"
    )
    hit_type_id = models.CharField(
            "HIT Type ID",
            max_length=255,
            null=True,
            blank=True,
            help_text="The ID of the HIT type of this HIT"
    )
    creation_time = models.DateTimeField(
            null=True,
            blank=True,
            help_text="The UTC date and time the HIT was created"
    )
    title = models.CharField(
            max_length=255,
            null=True,
            blank=True,
            help_text="The title of the HIT"
    )
    description = models.TextField(
            null=True,
            blank=True,
            help_text="A general description of the HIT",
    )
    keywords = models.TextField(
            "Keywords",
            null=True,
            blank=True,
            help_text=("One or more words or phrases that describe "
                       "the HIT, separated by commas."),
    )
    status = models.CharField(
            "HIT Status",
            max_length=1,
            choices=STATUS_CHOICES,
            null=True,
            blank=True,
            help_text="The status of the HIT and its assignments"
    )
    reward = models.DecimalField(
            max_digits=5,
            decimal_places=3,
            null=True,
            blank=True,
            help_text=("The amount of money the requester will pay a "
                       "worker for successfully completing the HIT")
    )
    lifetime_in_seconds = models.PositiveIntegerField(
            null=True,
            blank=True,
            help_text=("The amount of time, in seconds, after which the "
                       "HIT is no longer available for users to accept.")
    )
    assignment_duration_in_seconds = models.PositiveIntegerField(
            null=True,
            blank=True,
            help_text=("The length of time, in seconds, that a worker has "
                       "to complete the HIT after accepting it.")
    )
    max_assignments = models.PositiveIntegerField(
            null=True,
            blank=True,
            default=1,
            help_text=("The number of times the HIT can be accepted and "
                       "completed before the HIT becomes unavailable.")
    )
    auto_approval_delay_in_seconds = models.PositiveIntegerField(
            null=True,
            blank=True,
            help_text=("The amount of time, in seconds after the worker "
                       "submits an assignment for the HIT that the results "
                       "are automatically approved by the requester.")
    )
    requester_annotation = models.TextField(
            null=True,
            blank=True,
            help_text=("An arbitrary data field the Requester who created "
                       "the HIT can use. This field is visible only to the "
                       "creator of the HIT.")
    )
    number_of_similar_hits = models.PositiveIntegerField(
            null=True,
            blank=True,
            help_text=("The number of HITs with fields identical to this "
                       "HIT, other than the Question field.")
    )
    review_status = models.CharField(
            "HIT Review Status",
            max_length=1,
            choices=REVIEW_CHOICES,
            null=True,
            blank=True,
            help_text="Indicates the review status of the HIT."
    )
    number_of_assignments_pending = models.PositiveIntegerField(
            null=True,
            blank=True,
            help_text=("The number of assignments for this HIT that have "
                       "been accepted by Workers, but have not yet been "
                       "submitted, returned, abandoned.")
    )
    number_of_assignments_available = models.PositiveIntegerField(
            null=True,
            blank=True,
            help_text=("The number of assignments for this HIT that are "
                       "available for Workers to accept"),
    )
    number_of_assignments_completed = models.PositiveIntegerField(
            null=True,
            blank=True,
            help_text=("The number of assignments for this HIT that "
                       "have been approved or rejected.")
    )

    # To allow attachment of Generic Django instances
    content_type = models.ForeignKey(
            ContentType,
            verbose_name="Content type",
            related_name="hit",
            help_text=("Any Django model can be generically attached to "
                       "this HIT. This is the content type of that model "
                       "instance."),
            blank=True,
            null=True)

    content_id = models.PositiveIntegerField(
            "Content id",
            blank=True,
            null=True,
            help_text=("Any Django model can be generically attached to "
                       "this HIT. This is the id of that model instance."))
    attached_object = generic.GenericForeignKey(
            ct_field="content_type",
            fk_field="content_id",
            )

    def disable(self):
        """Disable/Destroy HIT that is no longer needed

        Remove a HIT from the Mechanical Turk marketplace, approves all
        submitted assignments that have not already been approved or
        rejected, and disposes of the HIT and all assignment data.

        Assignments for the HIT that have already been submitted, but
        not yet approved or rejected, will be automatically approved.
        Assignments in progress at the time of this method call  will be
        approved once the assignments are submitted. You will be charged
        for approval of these assignments. This method completely
        disposes of the HIT and all submitted assignment data.

        Assignment results data available at the time of this method
        call are saved in the Django models. However, additional
        Assignment results data cannot be retrieved for a HIT that has
        been disposed.

        It is not possible to re-enable a HIT once it has been disabled.
        To make the work from a disabled HIT available again, create a
        new HIT.

        This is a wrapper around the Boto API. Also see:
        http://boto.cloudhackers.com/en/latest/ref/mturk.html
        """
        # Check for new results and cache a copy in Django model
        self.update(do_update_assignments=True)
        self.connection.dispose_hit(self.mturk_id)

    def dispose(self):
        """Dispose of a HIT that is no longer needed.

        Only HITs in the "Reviewable" state, with all submitted
        assignments approved or rejected, can be disposed. This removes
        the data from Amazon Mechanical Turk, but not from the local
        Django database (i.e., a local cache copy is kept).

        This is a wrapper around the Boto API. Also see:
        http://boto.cloudhackers.com/en/latest/ref/mturk.html
        """
        # Don't waste time or resources if already marked as DISPOSED
        if self.status == self.DISPOSED:
            return

        # Check for new results and cache a copy in Django model
        self.update(do_update_assignments=True)

        # Verify HIT is reviewable
        if self.status != self.REVIEWABLE:
            #TODO: Excercise line
            raise DisposeException(
                    "Can't dispose of HIT (%s) that is still in %s status." % (
                        self.mturk_id,
                        dict(self.STATUS_CHOICES)[self.status]))

        # Verify Assignments are either APPROVED or REJECTED
        for assignment in self.assignments.all():
            if assignment.status not in [Assignment.APPROVED,
                    Assignment.REJECTED]:
                raise DisposeException(
                        "Can't dispose of HIT (%s) because Assignment "
                        "(%s) is not approved or rejected." % (
                            self.mturk_id, assignment.mturk_id))

        # Checks pass. Dispose of HIT and update status
        self.connection.dispose_hit(self.mturk_id)
        self.update()

    def expire(self):
        """Expire a HIT that is no longer needed as Mechanical Turk service

        The effect is identical to the HIT expiring on its own. The HIT
        no longer appears on the Mechanical Turk web site, and no new
        Workers are allowed to accept the HIT. Workers who have accepted
        the HIT prior to expiration are allowed to complete it or return
        it, or allow the assignment duration to elapse (abandon the HIT).
        Once all remaining assignments have been submitted, the expired
        HIT moves to the "Reviewable" state.

        This is a thin wrapper around the Boto API and taken from their
        documentation:
        http://boto.cloudhackers.com/en/latest/ref/mturk.html
        """
        self.connection.expire_hit(self.mturk_id)
        self.update()

    def extend(self, assignments_increment=None, expiration_increment=None):
        """Increase the maximum assignments or extend the expiration date

        Increase the maximum number of assignments, or extend the
        expiration date, of an existing HIT.

        NOTE: If a HIT has a status of Reviewable and the HIT is
        extended to make it Available, the HIT will not be returned by
        helpers.update_reviewable_hits() and its submitted assignments
        will not be returned by Assignment.update() until the HIT is
        Reviewable again. Assignment auto-approval will still happen on
        its original schedule, even if the HIT has been extended. Be
        sure to retrieve and approve (or reject) submitted assignments
        before extending the HIT, if so desired.

        This is a thin wrapper around the Boto API and taken from their
        documentation:
        http://boto.cloudhackers.com/en/latest/ref/mturk.html
        """
        self.connection.extend_hit(self.mturk_id,
                                   assignments_increment=assignments_increment,
                                   expiration_increment=expiration_increment)
        self.update()

    def set_reviewing(self, revert=None):
        """Toggle HIT status between Reviewable and Reviewing

        Update a HIT with a status of Reviewable to have a status of
        Reviewing, or reverts a Reviewing HIT back to the Reviewable
        status.

        Only HITs with a status of Reviewable can be updated with a
        status of Reviewing. Similarly, only Reviewing HITs can be
        reverted back to a status of Reviewable.

        This is a thin wrapper around the Boto API and taken from their
        documentation:
        http://boto.cloudhackers.com/en/latest/ref/mturk.html
        """
        self.connection.set_reviewing(self.mturk_id, revert=revert)
        self.update()

    def update(self, mturk_hit=None, do_update_assignments=False):
        """Update self with Mechanical Turk API data

        If mturk_hit is given to this function, it should be a Boto
        hit object that represents a Mechanical Turk HIT instance.
        Otherwise, Amazon Mechanical Turk is contacted to get additional
        information.

        This instance's attributes are updated.
        """
        if mturk_hit is None:
            hit = self.connection.get_hit(self.mturk_id)[0]
        else:
            assert isinstance(mturk_hit, boto.mturk.connection.HIT)
            hit = mturk_hit

        self.status = HIT.reverse_status_lookup[hit.HITStatus]
        self.reward = hit.Amount
        self.assignment_duration_in_seconds = hit.AssignmentDurationInSeconds
        self.auto_approval_delay_in_seconds = hit.AutoApprovalDelayInSeconds
        self.max_assignments = hit.MaxAssignments
        self.creation_time = amazon_string_to_datetime(hit.CreationTime)
        self.description = hit.Description
        self.title = hit.Title
        self.hit_type_id = hit.HITTypeId
        self.keywords = hit.Keywords
        if hasattr(self, 'NumberOfAssignmentsCompleted'):
            self.number_of_assignments_completed =\
                    hit.NumberOfAssignmentsCompleted
        if hasattr(self, 'NumberOfAssignmentsAvailable'):
            self.number_of_assignments_available =\
                    hit.NumberOfAssignmentsAvailable
        if hasattr(self, 'NumberOfAssignmentsPending'):
            self.number_of_assignments_pending =\
                    hit.NumberOfAssignmentsPending
        #'CurrencyCode', 'Reward', 'Expiration', 'expired']

        self.save()

        if do_update_assignments:
            for mturk_assignment in self.connection.get_assignments(
                                                               self.mturk_id):
                assert mturk_assignment.HITId == self.mturk_id
                djurk_assignment = Assignment.objects.get_or_create(
                        mturk_id=mturk_assignment.AssignmentId, hit=self)[0]
                djurk_assignment.update(mturk_assignment)

    class Meta:
        verbose_name = "HIT"
        verbose_name_plural = "HITs"

    def __unicode__(self):
        return u"HIT: %s" % self.mturk_id
pre_init.connect(init_connection_callback, sender=HIT)


class Assignment(models.Model):
    """An Amazon Mechanical Turk Assignment as a Django Model"""

    (_SUBMITTED, _APPROVED, _REJECTED) = ("Submitted", "Approved", "Rejected")
    (SUBMITTED, APPROVED, REJECTED) = ("S", "A", "R")

    STATUS_CHOICES = (
            (SUBMITTED, _SUBMITTED),
            (APPROVED, _APPROVED),
            (REJECTED, _REJECTED),
    )
    # Convenience lookup dictionaries for the above lists
    reverse_status_lookup = dict((v, k) for k, v in STATUS_CHOICES)

    mturk_id = models.CharField(
            "Assignment ID",
            max_length=255,
            unique=True,
            null=True,
            help_text="A unique identifier for the assignment"
    )
    worker_id = models.CharField(
            max_length=255,
            null=True,
            blank=True,
            help_text="The ID of the Worker who accepted the HIT"
    )
    hit = models.ForeignKey(
            HIT,
            null=True,
            blank=True,
            related_name='assignments',
    )
    status = models.CharField(
            max_length=1,
            choices=STATUS_CHOICES,
            null=True,
            blank=True,
            help_text="The status of the assignment"
    )
    auto_approval_time = models.DateTimeField(
            null=True,
            blank=True,
            help_text=("If results have been submitted, this is the date "
                       "and time, in UTC,  the results of the assignment are "
                       "considered approved automatically if they have not "
                       "already been explicitly approved or rejected by the "
                       "requester")
    )
    accept_time = models.DateTimeField(
            null=True,
            blank=True,
            help_text=("The date and time, in UTC, the Worker accepted "
                       " the assignment")
    )
    submit_time = models.DateTimeField(
            null=True,
            blank=True,
            help_text=("If the Worker has submitted results, this is the date "
                       "and time, in UTC, the assignment was submitted")
    )
    approval_time = models.DateTimeField(
            null=True,
            blank=True,
            help_text=("If requester has approved the results, this is the "
                       "date and time, in UTC, the results were approved")
    )
    rejection_time = models.DateTimeField(
            null=True,
            blank=True,
            help_text=("If requester has rejected the results, this is the "
                       "date and time, in UTC, the results were rejected")
    )
    deadline = models.DateTimeField(
            null=True,
            blank=True,
            help_text=("The date and time, in UTC, of the deadline for "
                       "the assignment")
    )
    requester_feedback = models.TextField(
            null=True,
            blank=True,
            help_text=("The optional text included with the call to either "
                       "approve or reject the assignment.")
    )

    def approve(self, feedback=None):
        """Thin wrapper around Boto approve function."""
        self.connection.approve_assignment(self.mturk_id, feedback=feedback)
        self.update()

    def reject(self, feedback=None):
        """Thin wrapper around Boto reject function."""
        self.connection.reject_assignment(self.mturk_id, feedback=feedback)
        self.update()

    def bonus(self, value=0.0, feedback=None):
        """Thin wrapper around Boto bonus function."""
        self.connection.grant_bonus(self.worker_id,
                                    self.mturk_id,
                                    boto.mturk.price.Price(amount=value),
                                    feedback=feedback)
        self.update()

    def update(self, mturk_assignment=None):
        """Update self with Mechanical Turk API data

        If mturk_assignment is given to this function, it should be
        a Boto assignment object that represents a Mechanical Turk
        Assignment instance.  Otherwise, Amazon Mechanical Turk is
        contacted.

        This instance's attributes are updated.
        """
        if mturk_assignment is None:
            hit = self.connection.get_hit(self.hit.mturk_id)[0]
            for a in self.connection.get_assignments(hit.HITId):
                # While we have the query, we may as well update
                if a.AssignmentId == self.mturk_id:
                    # That's this record. Hold onto so we can update below
                    assignment = a
                else:
                    other_assignment = Assignment.objects.get(
                            mturk_id=a.AssignmentId)
                    other_assignment.update(a)
        else:
            assert isinstance(mturk_assignment,
                              boto.mturk.connection.Assignment)
            assignment = mturk_assignment

        self.status = self.reverse_status_lookup[assignment.AssignmentStatus]
        self.worker_id = assignment.WorkerId
        self.submit_time = amazon_string_to_datetime(assignment.SubmitTime)
        self.accept_time = amazon_string_to_datetime(assignment.AcceptTime)
        self.auto_approval_time = amazon_string_to_datetime(
                assignment.AutoApprovalTime)
        self.submit_time = amazon_string_to_datetime(assignment.SubmitTime)

        # Different response groups for query
        if hasattr(assignment, 'RejectionTime'):
            self.rejection_time = amazon_string_to_datetime(
                    assignment.RejectionTime)
        if hasattr(assignment, 'ApprovalTime'):
            self.approval_time = amazon_string_to_datetime(
                    assignment.ApprovalTime)
        self.save()

        # Update any Key-Value Pairs that were associated with this
        # assignment
        for result_set in assignment.answers:
            for question in result_set:
                for key, value in question.fields:
                    kv = KeyValue.objects.get_or_create(key=key,
                                                        assignment=self)[0]
                    if kv.value != value:
                        kv.value = value
                        kv.save()

    def __unicode__(self):
        return self.mturk_id

    def __repr__(self):
        return u"Assignment: %s" % self.mturk_id
    __str__ = __unicode__
pre_init.connect(init_connection_callback, sender=Assignment)


class KeyValue(models.Model):
    """Answer/Key Value Pairs"""

    MAX_DISPLAY_LENGTH = 255

    key = models.CharField(
            max_length=255,
            help_text="The Key (variable) for a QuestionAnswer"
    )
    value = models.TextField(
            null=True,
            blank=True,
            help_text="The value associated with the key",
    )
    assignment = models.ForeignKey(
            Assignment,
            null=True,
            blank=True,
            related_name="answers",
    )

    def short_value(self):
        if len(self.value) > self.MAX_DISPLAY_LENGTH:
            return u'%s...' % self.value[:self.MAX_DISPLAY_LENGTH]
        else:
            return self.value
    short_value.short_description = "Value (%d chars)..." % MAX_DISPLAY_LENGTH

    class Meta:
        verbose_name = "Key-Value Pair"
        verbose_name_plural = "Key-Value Pairs"

    def __unicode__(self):
        return u"%s=%s" % (self.key, self.short_value())
