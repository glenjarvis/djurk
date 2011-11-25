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
API has an attribute 'HITId.' However, when modeled here, that attribute
has name 'hit_id.' An exception to that rule is that many string based
fields in the Mechanical Turk API return Nulls/Nones. Django prefers not
to allow CharFields to be nullable as both Null/None and the empty
string are redundant. As the API does return nullable data types, we
broke with Django convention on that point.
"""

from django.db import models


class HIT(models.Model):
    """An Amazon Mechanical Turk Human Intelligence Task as Django Model
   
    Note that although the Django convention is to avoid having nullable
    CharFields, this is allowed in these models as these are possible
    values that are returned from the Mechanical Turk API.
    """
    (ASSIGNABLE, UNASSIGNABLE, REVIEWABLE, REVIEWING, DISPOSED) = (
          'A', 'U', 'R', 'G', 'D')

    (_ASSIGNABLE, _UNASSIGNABLE, _REVIEWABLE, _REVIEWING, _DISPOSED) = (
          "Assignable", "Unassignable", "Reviewable", "Reviewing", "Disposed")

    (NOT_REVIEWED, MARKED_FOR_REVIEW, REVIEWED_APPROPRIATE,
          REVIEWED_INAPPROPRIATE) = ("N", "M", "R", "I")

    (_NOT_REVIEWED, _MARKED_FOR_REVIEW, _REVIEWED_APPROPRIATE,
          _REVIEWED_INAPPROPRIATE) = ("NotReviewed", "MarkedForReview",
          "ReviewedAppropriate","ReviewedInappropriate")

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
    reverse_status_lookup = dict((v,k) for k,v in STATUS_CHOICES)
    reverse_review_lookup = dict((v,k) for k,v in REVIEW_CHOICES)

    hit_id = models.CharField(
            "HIT ID",
            max_length=128,
            null=True,
            help_text="A unique identifier for the HIT"
    )
    hit_type_id = models.CharField(
            "HIT Type ID",
            max_length=128,
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
            max_length=128,
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
    hit_status = models.CharField(
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
    assignment_duration_in_seconds= models.PositiveIntegerField(
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
    hit_review_status = models.CharField(
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

    def __unicode__(self):
        return u"HIT: %s" % self.hit_id
