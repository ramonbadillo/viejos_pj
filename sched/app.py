from flask import Flask

app = Flask(__name__)


@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
    return 'Detail of appointment #{}.'.format(appointment_id)


@app.route(
    '/appointments/<int:appointment_id>/edit/',
    methods=['GET', 'POST'])
#@app.route(...) and def appointment_edit(...).
# def appointment_edit(appointment_id):
# return 'Form to edit appointment #.'.format(appointment_id)
@app.route(
    '/appointments/create/',
    methods=['GET', 'POST'])
def appointment_create():
    return 'Form to create a new appointment.'


#@app.route('/ appointments / <int: appointment_id > /delete /, methods=['DELETE'])
#def appointment_delete(appointment_id):
#    raise NotImplementedError('DELETE')

if __name__ == '__main__':
    manager.run()
