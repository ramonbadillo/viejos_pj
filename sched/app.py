from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, logout_user, login_required

from models import Base
from forms import AppointmentForm, LoginForm
from models import Appointment
import filters
from models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sched.db'
app.secret_key = 'secret_key'

# Use Flask-SQLAlchemy for its engine and session
# configuration. Load the extension, giving it the app object,
# and override its default Model class with the pure
# SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base

filters.init_app(app)


# Use Flask-Login to track current user in Flask's session.
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login hook to load a User instance from ID."""
    return db.session.query(User).get(user_id)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    validarUsuario()

    form = LoginForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        email = form.username.data.lower().strip()
        password = form.password.data.lower().strip()
        user, authenticated = User.authenticate(
            db.session.query, email, password)

        if authenticated:
            login_user(user)
            return redirect(url_for('appointment_list'))
        else:
            error = 'Incorrect username or password.'

    return render_template('user/login.html', form=form, error=error)


def validarUsuario():
    if current_user.is_authenticated():
        return redirect(url_for('appointment_list'))


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/appointments/')
@login_required
def appointment_list():
    """
    Provide HTML listing of all appointments
    """
    # Query: Get all Appointment objects, sorted by date.
    appts = (db.session.query(Appointment)
             .order_by(Appointment.start.asc()).all())
    return render_template('appointment/index.html', appts=appts)


@app.route('/appointments/<int:appointment_id>/')
@login_required
def appointment_detail(appointment_id):
    """
    Muestra el detalle de una cita en especifico
    """
    # Query: get Appointment object by ID.
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        # Abort with Not Found.
        abort(404)
    return render_template('appointment/detail.html', appt=appt)


@app.route('/appointments/<int:appointment_id>/edit/',
           methods=['GET', 'POST'])
@login_required
def appointment_edit(appointment_id):
    """
    Provide HTML form to edit a given appointment
    """
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        abort(404)
    form = AppointmentForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view.
        return redirect(url_for('appointment_detail', appointment_id=appt.id))
    # Either
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/create/', methods=['GET', 'POST'])
@login_required
def appointment_create():
    """
    Provide HTML form to create a new appointment.
    """
    form = AppointmentForm(request.form)
    if request.method == 'POST' and form.validate():

        appt = Appointment(user_id=current_user.id)
        if appt.user_id != current_user.id:
            abort(403)

        form.populate_obj(appt)
        print("Start: {}".format(appt.start))

        db.session.add(appt)
        db.session.commit()
        # Success. Send user back to full appointment list.
        return redirect(url_for('appointment_list'))
    # Either first load or validation error at this point.
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
@login_required
def appointment_delete(appointment_id):
    """Delete record using HTTP DELETE, respond with JSON."""
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        abort(404)
    db.session.delete(appt)
    db.session.commit()
    return jsonify({'status': 'OK'})


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def error_not_found(error):
    return render_template('error/not_found.html'), 404


@app.errorhandler(405)
def error_not_allowed(error):
    return render_template('error/not_allowed.html'), 405

if __name__ == '__main__':
    app.run(debug=True)
