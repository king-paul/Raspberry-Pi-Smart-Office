from flask_wtf import Form, FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, InputRequired
import json, requests, subprocess

from globals import get_ip

ip = get_ip()

def get_doctors():
    """
    This function is used to make a call to the crud API to return all doctors. I then returns a dictionary containing the id and name of each one.
    This is intended for use with a dropdown combo box on a web form/
    """

    patient_response = requests.get('http://{}:5001/doctor'.format(ip))
    doctors = json.loads(patient_response.text)

    id = 0

    # doctor_names = dict()
    doctor_names = {'1': {},
                    '2': {},
                    '3': {},
                    '4': {},
                    '5': {},
                    '6': {},
                    '7': {},
                    '8': {},
                    '9': {},
                    '10': {},
                    '11': {},
                    '12': {},
                    '13': {},
                    '14': {},
                    '15': {},
                    '16': {},
                    '17': {},
                    '18': {},
                    '19': {},
                    '20': {}
    }

    # for doctor in doctors:
    #     # print(doctor)
    #     id += 1
    #     print('{}: {} {}'.format(id, doctor['first_name'], doctor['last_name']))

    # for doctor in doctors:
    #     '{}'.format(id) :

    for doctor in doctors:
        id +=1
        doctor_names['{}'.format(id)]['name'] = doctor['first_name'] + ' ' + doctor['last_name']

    # return [(doctor_names['id'], doctor_names['name']) for doctor in doctors]
    return doctor_names

class PatientForm(FlaskForm):
    """ 
    This is a Flask WTF form used to create a patient registraion from and validate it.
    It is rendered on the patients.html page via the '/patients' route.
    
    To use this class make a call to PatientForm()
    """

    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', [validators.DataRequired(), validators.Length(min=6, max=35), validators.Email()])
    phone = StringField('Telephone Nmber', [validators.DataRequired(), validators.Length(min=8, max=12)])
    address = StringField('Address')

    submit = SubmitField('register')

#for sving notes
class NotesForm(FlaskForm):
    note = TextAreaField('notes', validators=[DataRequired()])
    symptoms = TextAreaField('symptoms')
    patient_id = StringField('patient_id')
    Submit = SubmitField('save')

# class AppointmentForm(FlaskForm):
#     doctor = SelectField(
#         'Select Doctor',
#         choices = ['', '', '']
#         )

#     doctor_id = IntegerField('Doctor Id', validators=[DataRequired()])
#     start_time = DateTimeField('Start Time', validators=[DataRequired()])
#     end_time = DateTimeField('End Time', validators=[DataRequired()])
#     description = StringField('Description', [validators.Length(min=50, max=2048)])

class AppointmentForm(FlaskForm):
    """ 
    This is a Flask WTF form used to create a appointment scheduling from and validate it.
    It is rendered on the patient.html page via the '/patients/<id>' route.
    
    To use this class make a call to AppointmentForm()
    """
    
    doctors = get_doctors()

    # print(doctors)

    doctor = SelectField(
        'Select Doctor',
        choices = [(1, 'Doctor 1'), (2, 'Doctor 2'), (3, 'Doctor 3')]
        # choices = [doctors]
        )
    doctor_id = IntegerField('Doctor Id', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d')
    start_time = DateTimeField('Start Time', validators=[DataRequired()])
    end_time = DateTimeField('End Time', validators=[DataRequired()])
    description = TextAreaField('Description', [validators.Length(min=50, max=2048)])

class ClerkForm(FlaskForm):
    first_name = StringField('First Name:', validators=[InputRequired()])
    last_name = StringField('Last Name',  validators=[InputRequired()])
    email = StringField('Email Address', validators=[InputRequired(), validators.Length(min=6, max=35)])
    date = DateTimeField('Date', format='%d-%m-%Y', validators=[DataRequired()])
    start_time = DateTimeField('Time', format='%H:%M', validators=[DataRequired()])
    end_time = DateTimeField('Time', format='%H:%M', validators=[DataRequired()])
    doctor = SelectField('Select Doctor', choices=[('1', 'Doctor 1'), ('2', 'Doctor 2'), ('3', 'Doctor 3') ])
    description = TextAreaField('Appointment Details', validators=[InputRequired()])

    submitAppt = SubmitField('submit')
