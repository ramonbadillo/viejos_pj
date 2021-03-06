import unittest
import json
import sched.app as app
import sched.models as models
import sched.forms as forms
import sched.filters as filters
from datetime import datetime, date, timedelta
from jinja2 import Environment


class filterTests(unittest.TestCase):

    def testDatetimeEmpty(self):
        result = filters.do_datetime(None)
        self.assertEqual(result, '')

    def testDatetimeWithoutHour(self):
        dat = date(2014, 1, 23)
        result = filters.do_datetime(dat)
        self.assertEqual(result, '2014-01-23 - Thursday at 12:00am')

    def testDatetimeWithHour(self):
        date = datetime(2014, 1, 23, 9, 00, 00)
        result = filters.do_datetime(date)
        self.assertEqual(result, '2014-01-23 - Thursday at 9:00am')

    def testDateEmpty(self):
        result = filters.do_date(None)
        self.assertEqual(result, '')

    def testDateNotEmpty(self):
        date = datetime(2014, 1, 23, 9, 00, 00)
        result = filters.do_date(date)
        self.assertEqual(result, '2014-01-23 - Thursday')

    def testDurationHour(self):
        result = filters.do_duration(3600)
        self.assertEqual(result, '0 days, 1 hours, 0 minutes, 0 seconds')

    def testdurationMinutes(self):
        result = filters.do_duration(60)
        self.assertEqual(result, '0 days, 0 hours, 1 minutes, 0 seconds')

    def testnl2brWithoutMarkup(self):
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

    def testAppForm(self):
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

    def testLoginForm(self):
        form = forms.LoginForm()
        self.assertEqual(
            '<input id="username" name="username" type="text" value="">', str(
                form.username))
        self.assertEqual(
            '<input id="password" name="password" type="password" value="">',
            str(form.password))


class modelsTest(unittest.TestCase):

    def testAppointment1(self):
        date = datetime.now()
        appointmentT = models.Appointment(
            title='Clase viejo', start=date, end=date +
            timedelta(seconds=3600), allday=False)
        self.assertNotEqual('<Appointment: 4>', appointmentT.__repr__())

    def testUserPassword(self):
        user = models.User(name="Viejo", email="adios@hola.com")
        user._set_password("12346")
        assert "sha1" in user._get_password()
        self.assertNotEqual(user._get_password(), "12346")
        self.assertEqual(True, user.check_password("12346"))

    def testUserNoPassword(self):
        user = models.User(name="Viejo", email="adios@hola.com")
        self.assertEqual(False, user.check_password("12346"))

    def testUserStatus(self):
        user = models.User(name="Viejo", email="adios@hola.com")
        user._set_password("12346")
        self.assertNotEqual(user.get_id(), 0)
        self.assertNotEqual(user.is_active(), False)

    def testUserAuthenticate(self):
        user, authenticate = models.User.authenticate(
            app.db.session.query, "hola@adios.com", "12345")
        self.assertNotEqual(user, None)
        self.assertNotEqual(authenticate, False)


class appTests(unittest.TestCase):

    def setUp(self):
        self.appointmentT = app.app.test_client()

    def testAppoitmentList(self):
        response = self.appointmentT.get("/appointments")
        self.assertEquals(response.status_code, 301)
        assert 'Redirecting' in response.data

    def testLogin(self):
        response = self.appointmentT.get("/login/")
        self.assertEquals(response.status_code, 200)
        assert 'Log user' in response.data
        response = self.appointmentT.post('login', data=dict(
            username='hola@adios.com', password='12345'),
            follow_redirects=True)
        self.assertEquals(response.status_code, 200)

    def testLogin2(self):
        response = self.appointmentT.post('/login/', data=dict(
            username="adios@hola.com", password='12346'),
            follow_redirects=True)
        self.assertEquals(response.status_code, 200)

    def testLogout(self):
        response = self.appointmentT.get("/logout/")
        self.assertEquals(response.status_code, 302)
        assert 'Redirecting' in response.data

    def testAppoitmentDetail(self):
        response = self.appointmentT.post('/login/', data=dict(
            username='hola@adios.com', password='12345'),
            follow_redirects=True)
        response = self.appointmentT.get('/appointments/2/')
        self.assertEquals(response.status_code, 200)
        assert "New appointment2" in response.data
        assert "algo que no es" not in response.data

    def testFalseAppointment(self):
        response = self.appointmentT.post('/login/', data=dict(
            username='hola@adios.com', password='12345'),
            follow_redirects=True)
        response = self.appointmentT.get('/appointments/0/')
        self.assertEquals(response.status_code, 404)
        assert "Not Found" in response.data

    def testAppoitmentEdit(self):
        response = self.appointmentT.post('/login/', data=dict(
            username='hola@adios.com', password='12345'),
            follow_redirects=True)
        response = self.appointmentT.get('/appointments/1/edit/')
        self.assertEquals(response.status_code, 200)
        assert "Edit Appointment" in response.data

        response = self.appointmentT.post('/appointments/1/edit/', data=dict(
            title="New appointment", start="2014-01-23 12:00:00",
            end="2014-01-23 23:00:00", location="CIMAT",
            description="Fiesta"), follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        assert "New appointment" in response.data

    def testFalseAppointmentEdit(self):
        response = self.appointmentT.post('/login/', data=dict(
            username='hola@adios.com', password='12345'),
            follow_redirects=True)
        response = self.appointmentT.get('/appointments/0/edit/')
        self.assertEquals(response.status_code, 404)
        assert "Not Found" in response.data

    def testAppoitmentCreate(self):
        response = self.appointmentT.post('/login/', data=dict(
            username='hola@adios.com', password='12345'),
            follow_redirects=True)
        response = self.appointmentT.get('/appointments/create/')
        self.assertEquals(response.status_code, 200)
        assert "Add Appointment" in response.data

        response = self.appointmentT.post('/appointments/create/', data=dict(
            title="New appointment", start="2014-01-23 12:00:00",
            end="2014-01-23 23:00:00", location="CIMAT",
            description="Fiesta"), follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        assert "New appointment" in response.data

    def testAppoitmentDelete(self):
        response = self.appointmentT.post('/login/', data=dict(
            username='hola@adios.com', password='12345'),
            follow_redirects=True)
        response = self.appointmentT.get('/appointments/1/delete/')
        self.assertEquals(response.status_code, 405)
        assert "Not Allowed" in response.data

        response = self.appointmentT.delete('/appointments/3/delete/',
                                            follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'status': 'OK'})

        response = self.appointmentT.delete('/appointments/666/delete/',
                                    follow_redirects=True)
        self.assertEquals(response.status_code, 404)
        assert "Not Found" in response.data

    def testIndex(self):
        response = self.appointmentT.post('/login/', data=dict(
            username='email@cimat.mx', password='thepassword'),
            follow_redirects=True)

        response = self.appointmentT.get('/')
        self.assertEquals(response.status_code, 200)
        assert "Appointment scheduler" in response.data

if __name__ == '__main__':
    unittest.main()