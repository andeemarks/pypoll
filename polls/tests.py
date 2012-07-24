from django.utils import unittest, timezone
from polls.models import Poll
import datetime
from django.test import Client, TestCase

class PollTestCase(unittest.TestCase):
  def setUp(self):
    self.poll = Poll.objects.create(question="new", pub_date=timezone.now())

  def test_new_polls_were_published_recently(self):
    """Poll less than 1 day old are considered to have been published recently"""
    self.assertTrue(self.poll.was_published_recently())

  def test_old_polls_were_not_published_recently(self):
    """Poll more => 1 day old are not considered to have been published recently"""
    self.poll.pub_date -= datetime.timedelta(days=1)
    self.assertFalse(self.poll.was_published_recently())

  def test_1_day_old_polls_were_published_recently(self):
    """Poll < 1 day old are considered to have been published recently"""
    self.poll.pub_date -= datetime.timedelta(hours=23, minutes=59, seconds=59)
    self.assertTrue(self.poll.was_published_recently())

class ViewPollsTestCase(TestCase):
  def setUp(self):
    self.c = Client()
    self.test_poll = Poll.objects.create(question="Test poll", pub_date=timezone.now())

  def test_access_to_list_polls_page(self):
    """Main entry point to app is responsive"""
    response = self.c.get('/polls/')
    self.assertContains(response, "Test poll")

  def test_access_to_specific_polls_page(self):
    """Poll entry point is responsive"""
    response = self.c.get('/polls/%d/' % self.test_poll.pk)
    self.assertContains(response, "Test poll")

  def test_access_to_admin_page(self):
    """Admin entry point is responsive"""
    response = self.c.get('/admin/')
    self.assertEqual(response.status_code, 200)
