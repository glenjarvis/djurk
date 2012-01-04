#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Cron job to constantly poll Amazon Mechanical Turk"""


from optparse import make_option

from django.core.management.base import BaseCommand
from boto.mturk.question import (AnswerSpecification, Overview, Question,
        QuestionContent, QuestionForm, FreeTextAnswer, FormattedContent)

from djurk.common import get_connection


def demo_create_favorite_color_hit(use_sandbox=False):
    """A HIT to determine the Worker's favorite color"""

    TITLE = 'Tell me your favorite color'
    DESCRIPTION = ('This is a HIT that is created by a computer program '
                   'to demonstrate how Mechanical Turk works. This should '
                   'be a free HIT for the worker.')
    KEYWORDS = 'data collection, favorite, color'
    DURATION = 15 * 60  # 15 minutes (Time to work on HIT)
    MAX_ASSIGNMENTS = 1  # Number of assignments per HIT
    REWARD_PER_ASSIGNMENT = 0.01  # $0.01 USD (1 cent)

    #--------------- BUILD HIT container -------------------
    overview = Overview()
    overview.append_field('Title', TITLE)
    overview.append(FormattedContent(
         "<p>This is an experiment to learn Mechanical Turk</p>"))

    #---------------  BUILD QUESTION 1 -------------------
    question_content = QuestionContent()
    question_content.append(FormattedContent(
         "<b>What is your favorite color?</b>"))

    free_text_answer = FreeTextAnswer(num_lines=1)

    q1 = Question(identifier='favorite_color',
                  content=question_content,
                  answer_spec=AnswerSpecification(free_text_answer),
                  is_required=True)

    #---------------  BUILD QUESTION 3 -------------------
    question_content = QuestionContent()
    question_content.append(FormattedContent(
        """<p>Give me a fun comment:</p>"""))

    q2 = Question(identifier="comments",
                  content=question_content,
                  answer_spec=AnswerSpecification(FreeTextAnswer()))

    #--------------- BUILD THE QUESTION FORM -------------------
    question_form = QuestionForm()
    question_form.append(overview)
    question_form.append(q1)
    question_form.append(q2)

    #--------------- CREATE THE HIT -------------------
    mtc = get_connection(use_sandbox=use_sandbox)
    hit = mtc.create_hit(questions=question_form,
                         max_assignments=MAX_ASSIGNMENTS,
                         title=TITLE,
                         description=DESCRIPTION,
                         keywords=KEYWORDS,
                         duration=DURATION,
                         reward=REWARD_PER_ASSIGNMENT)

    #---------- SHOW A LINK TO THE HIT GROUP -----------
    if use_sandbox:
        base = "https://workersandbox.mturk.com" 
    else:
        base = "https://www.mturk.com" 

    print "\nVisit this website to see HITs that were created:"
    print "%s/mturk/preview?groupId=%s" % (base, hit[0].HITTypeId)

    return hit[0]

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
        '--account-balance',
        action='store_true',
        dest='account_balance',
        default=False,
        help='Print account balance '),
        make_option(
        '--sample-hit',
        action='store_true',
        dest='sample_hit',
        default=False,
        help=('Create sample "favorite color" hit')),
        make_option(
        '--sandbox',
        action='store_true',
        dest='sandbox',
        default=False,
        help='Use Amazon Mechanical Turk Sandbox (instead of production)'),
    )

    def check_account_balance(self):
        print self.mtc.get_account_balance()

    def handle(self, *args, **options):
        self.use_sandbox = options['sandbox']
        self.mtc = get_connection(use_sandbox=self.use_sandbox)

        if options['account_balance']:
            self.check_account_balance()

        if options['sample_hit']:
            demo_create_favorite_color_hit(use_sandbox=self.use_sandbox)
