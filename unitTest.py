import unitttest
import json
import sched.app as app
import sched.models as models
import sched.forms as forms
import sched.filters as filters
from datetime import datetime, date, timedelta
from jinja2 import Enviroment

class filterTests(unittest.TestCase):

	def datetimeEmpty(self):
		date = filters-do_datetime(None)
		self.assertNotEqual(fecha, "Today")
		self.assertEqual(fecha, '')

if __name == '__main__':
	unittest.main()