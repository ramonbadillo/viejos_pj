import unittest
import json
import sched.app as app
import sched.models as models
import sched.forms as forms
import sched.filters as filters
from datetime import datetime, date, timedelta
from jinja2 import Enviroment

class filterTests(unittest.TestCase):

	def datetimeEmpty(self):
		result = filters.do_datetime(None)
		self.assertEqual(result, '')

	def datetimeWithoutHour(self):
		date = date(2014, 01, 23)
		result = filters.do_datetime(date)
		self.assertEqual(result, '2014-01-23 - Thursday')

	def datetimeWithHour(self):
		date = datetime(2014, 01, 23, 9, 00, 00)
		result = filters.do_datetime(date)
		self.assertEqual((result, '2014-01-23 - Thursday at 9:00am'))

	def dateEmpty(self):
		result = filters.date(None)
		self.assertEqual(result, '')

	def dateNotEmpty(self):
		date = datetime(2014, 01, 23, 9, 00, 00)
		result = filters.do_date(date)
		self.assertEqual(result, '2014-01-23 - Thursday')

	def durationHour(self):
		result = filters.do_duration(3600)
		self.assertEqual(time, '0 days, 1 hours, 0 minutes, 0 seconds')

	def durationMinutes(self):
		result = filters.do_duration(60)
		self.assertEqual(time, '0 days, 0 hours, 1 minutes, 0 seconds')

	def test_do_nl2br_without_Markup(self):
		template_env = Environment(
			autoescape=False,
			extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'])
		text = "Texto con '\n' para saltos '\n' pero junto"
		changes = filters.do_nl2br(template_env, text)
		self.assertNotEqual(changes, "")
		self.assertEqual(changes, "Texto con &#39;<br />&#39; para saltos &#39;<br />&#39; pero junto")
		
	def test_do_nl2br_with_Markup(self):
		template_env = Environment(
			autoescape=True,
			extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'])
		text = "Texto con '\n' para saltos '\n' pero <script>junto</script>"
		changes = filters.do_nl2br(template_env, text)
		self.assertNotEqual(changes, "Texto con &#39;<br />&#39; para saltos &#39;<br />&#39; pero junto")
		self.assertEqual(changes, "Texto con &#39;<br />&#39; para saltos &#39;<br />&#39; pero &lt;script&gt;junto&lt;/script&gt;")


if __name == '__main__':
	unittest.main()