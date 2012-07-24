from django.utils import unittest
from polls.models import Poll
import datetime
from django.utils import timezone

class PollTestCase(unittest.TestCase):
    # def setUp(self):

    def test_new_polls_were_published_recently(self):
        """Poll less than 1 day old are considered to have been published recently"""
        self.new_poll = Poll.objects.create(question="new", pub_date=timezone.now())
        self.assertEqual(self.new_poll.was_published_recently(), True)

    def test_old_polls_were_not_published_recently(self):
        """Poll more than 1 day old are not considered to have been published recently"""
        self.old_poll = Poll.objects.create(question="new", pub_date=timezone.now() - datetime.timedelta(days=3))
        self.assertEqual(self.old_poll.was_published_recently(), False)

    def test_1_day_old_polls_were_published_recently(self):
        """Poll exactly 1 day old are considered to have been published recently"""
        self.old_poll = Poll.objects.create(question="new", pub_date=timezone.now() - datetime.timedelta(days=1))
        self.assertEqual(self.old_poll.was_published_recently(), True)
