"""
    This file is contains all the flask routes to different webpages including the processes the run behind them.
"""
import json, requests, subprocess
from app import app
import json, requests

from globals import get_ip
from datetime import datetime
from flask import render_template, request, redirect
# from app.add2calendar import add_appointment
from app.forms import *
from sqlalchemy import func

# app.config['SECRET_KEY'] = '123456SECRET'

# returns the lan ip address in ipv4 format
ip = get_ip()

# main route
@app.route("/")
def index():
    """
        Reads database tables and directs user to the home page, rendering tables from the JSON reuqests.
    """
    # get all the json data from the patient table
    response = requests.get('http://{}:5001/patient'.format(ip))
    patients = json.loads(response.text)

    # get all the josn data from doctors table
    response = requests.get('http://{}:5001/doctor'.format(ip))
    doctors = json.loads(response.text)

    response = requests.get('http://{}:5001/appointment'.format(ip))
    appointments = json.loads(response.text)
    return render_template('index.html', patients=patients, doctors=doctors, appointments=appointments)

@app.route("/patients/", methods=['GET', 'POST'])
def patients():
	"""
	Creates a new PatientForm object and directs the user to the patient registraion page, passing the form object to it.
	When the form has been validated and submitted, a post request is made to the API adding a new doctor and the use is
	directed to the confirmation page with the details from the form passed to it.
	"""
	# instaniate a new patient form
	form = PatientForm()
	
	if form.validate_on_submit():
		
		formData = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "telephone": request.form['phone'],
            "address": request.form['address']
        }
		
		print(formData)
		
		requests.post('http://{}:5001/patient'.format(ip), json=formData)
		return redirect('confirmation.html')
		# return redirect("/patients/{}".format(formData))
	
	return render_template('patients.html', form=form, ip=ip)

@app.route("/patients/<form>", methods=['GET'])
def register_confirmation(formData):
	return render_template('confirmation.html', patient=formData)

@app.route("/patients/<id>")
def patient(id=None):
    """
        Directs the user to the single patient page after collecting data for a particular id using JSON requests.
    """
    patient_response = requests.get('http://{}:5001/patient/{}'.format(ip, id))
    patient = json.loads(patient_response.text)

    form = AppointmentForm()

    firstName = patient['first_name']
    lastName = patient['last_name']

    return render_template("single-entity/patient.html", id=id, firstName=firstName, lastName=lastName, form=form)

    # appointments_response = requests.get('http://{}:5001/patient-appointment/{}'.format(ip, id))
    # appointments = json.loads(appointments_response.text)
    # appointments = None

    # if form.validate_on_submit():

    #     print('Entered validation block')

    #     formData = {
    #         "patient_id": id,
    #         "doctor_id": request.form['doctor_id'],
    #         "start_time": request.form['start_time'],
    #         "end_time": request.form['end_time'],
    #         "description": request.form['description'],
    #     }

    #     print(formData)

    #     requests.post('http://{}:5001/appointment'.format(ip), json=formData)

# appointments=appointments)

@app.route("/doctors/")
def doctors():
	"""
	Directs the user to the doctors page
	"""
	patient_table_response = requests.get('http://{}:5001/patient'.format(ip))
	patient_table = json.loads(patient_table_response.text)
	
	notes_Table_response = requests.get('http://{}:5001/notes'.format(ip))
	notes_Table = json.loads(notes_Table_response.text)
	return render_template('doctors.html',patients = patient_table,notes = notes_Table)


@app.route("/clerks/", methods=['GET', 'POST'])
def submitAppt():
	"""
	Directs the user to the medical clerks page
	"""
	form = ClerkForm()
	response = requests.get('http://{}:5001/appointment'.format(ip))
	appointments = json.loads(response.text)
	
	if form.validate_on_submit():
		
		formData = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "date": request.form['date'],
            "start_time": request.form['start_time'],
            "end_time": request.form['end_time'],
            "doctor": request.form['doctor'],
            "description": request.form['description']
        }		
		print(formData)
		
		requests.post('http://{}:5001/appointment'.format(ip), json=formData)
		return redirect('appt_confirmation.html')
		
	return render_template('clerks.html', form=form,  appointments=appointments)

@app.route("/appointment", methods = ['POST'])
def appointments():
	"""
	Directs the user to the doctors page
	"""
	patient_table_response = requests.get('http://{}:5001/patient'.format(ip))
	patient_table = json.loads(patient_table_response.text)
	
	notes_Table_response = requests.get('http://{}:5001/notes'.format(ip))
	notes_Table = json.loads(notes_Table_response.text)
	return render_template('doctors.html',patients = patient_table,notes = notes_Table)

@app.route("/notes/<string:name>",methods=['GET','POST'])
def notes(name):
	"""
	directes doctor to form for making notes on patients
	TO DO : 
			edit crud
	"""
	form = NotesForm()
	

	if form.validate_on_submit():
		print(request.form['note'])
		print(request.form['symptoms'])
		print(request.form['patient_id'])
		data = {
			"notes": request.form['note'],
			"patient_id": request.form['patient_id'],
			"symptoms": request.form['symptoms']
		}
		
		print(data)
		requests.post('http://{}:5001/notes'.format(ip), json=data)
		return redirect('doctors/')
	else:
		patient_response = requests.get('http://{}:5001/patient'.format(ip))
		patient_list = json.loads(patient_response.text)
		fName = str()
		lName = str()
		i = 0
		id = 0
		for patient in patient_list:
			firstName = patient['first_name']
			lastName = patient['last_name']
			compare = firstName+lastName
			if name == compare:
				id = i
				fName = firstName
				lName = lastName
			
			i=i+1
		return render_template('notes.html',id=id,firstName=fName, lastName=lName, form = form)
