import unittest
# import json
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
        dat = date(2014, 1, 23)
        result = filters.do_datetime(dat)
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
        self.assertEqual(result, '0 days, 1 hours, 0 minutes, 0 seconds')

    def durationMinutes(self):
        result = filters.do_duration(60)
        self.assertEqual(result, '0 days, 0 hours, 1 minutes, 0 seconds')

    def nl2brWithoutMarkup(self):
        template_env = Environment(
            autoescape=False,
            extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'])
        text = "AAAA '\n' BBBB '\n' CCCC"
        changes = filters.do_nl2br(template_env, text)
        self.assertNotEqual(changes, "")
        self.assertEqual(
            changes,
            "AAAA &#39;<br />&#39; BBBB &#39;<br />&#39; "
            "CCCC")


class formTests(unittest.TestCase):

    def appForm(self):
        form = forms.AppointmentForm()
        self.assertEqual(
            '<input id="title" name="title" type="text" value="">', str(
                form.title))
        self.assertEqual(
            '<input id="start" name="start" type="text" value="">', str(
                form.start))
        self.assertEqual(
            '<input id="end" name="end" type="text" value="">', str(form.end))
        self.assertEqual(
            '<input id="allday" name="allday" type="checkbox" value="y">', str(
                form.allday))
        self.assertEqual(
            '<input id="location" name="location" type="text" value="">', str(
                form.location))
        self.assertEqual(
            '<textarea id="description" name="description"></textarea>', str(
                form.description))

    def loginForm(self):
        form = forms.LoginForm()
        self.assertEqual(
            '<input id="username" name="username" type="text" value="">', str(
                form.username))
        self.assertEqual(
            '<input id="password" name="password" type="password" value="">',
            str(form.password))


class modelsTest(unittest.TestCase):

    def appointment1(self):
        date = datetime.now()
        appointmentT = models.Appointment(
            title='Clase viejo', start=date, end=date +
            timedelta(seconds=3600), allday=False)
        self.assertNotEqual('<Appointment: 4>', appointmentT.__repr__())

    def userPassword(self):
        user = models.User(name="Viejo", email="adios@hola.com")
        user._set_password("12346")
        assert "64321" in user._get_password()
        self.assertNotEqual(user._get_password(), "12346")
        self.assertEqual(True, user.check_password("12346"))

    def userNoPassword(self):
        user = models.User(name="Viejo", email="adios@hola.com")
        self.assertEqual(False, user.check_password("12346"))

    def userStatus(self):
        user = models.User(name="Viejo", email="adios@hola.com")
        user._set_password("12346")
        self.assertNotEqual(user.get_id(), 0)
        self.assertNotEqual(user.is_active(), False)

    def userAuthenticate(self):
        user, authenticate = models.User.authenticate(
            app.db.session.query, "hola@adios.com", "12345")
        self.assertNotEqual(user, None)
        self.assertNotEqual(authenticate, False)
if __name__ == '__main__':
    unittest.main()
