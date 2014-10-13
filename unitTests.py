import unittest
import json
import sched.app as app
import sched.models as models
import sched.forms as forms
import sched.filters as filters
from datetime import datetime, date, timedelta
from jinja2 import Environment

class filterTests(unittest.TestCase):

	def datetimeEmpty(self):
		result = filters.do_datetime(None)
		self.assertEqual(result, '')

	def datetimeWithoutHour(self):
		date = date(2014, 1, 23)
		result = filters.do_datetime(date)
		self.assertEqual(result, '2014-01-23 - Thursday')

	def datetimeWithHour(self):
		date = datetime(2014, 1, 23, 9, 00, 00)
		result = filters.do_datetime(date)
		self.assertEqual((result, '2014-01-23 - Thursday at 9:00am'))

	def dateEmpty(self):
		result = filters.date(None)
		self.assertEqual(result, '')

	def dateNotEmpty(self):
		date = datetime(2014, 1, 23, 9, 00, 00)
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

class testForm(unittest.TestCase):
	
	def test_form_Appt(self):
		form = forms.AppointmentForm()
		self.assertEqual(
			'<input id="title" name="title" type="text" value="">', str(form.title))
		self.assertEqual(
			'<input id="start" name="start" type="text" value="">', str(form.start))
		self.assertEqual(
			'<input id="end" name="end" type="text" value="">', str(form.end))
		self.assertEqual(
			'<input id="allday" name="allday" type="checkbox" value="y">', str(form.allday))
		self.assertEqual(
			'<input id="location" name="location" type="text" value="">', str(form.location))
		self.assertEqual(
			'<textarea id="description" name="description"></textarea>', str(form.description))
	def test_form_Login(self):
		form = forms.LoginForm()
		self.assertEqual(
			'<input id="username" name="username" type="text" value="">', str(form.username))
		self.assertEqual(
			'<input id="password" name="password" type="password" value="">', str(form.password))


if __name__ == '__main__':
	unittest.main()