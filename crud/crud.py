
import sys
from flask import redirect
from connection import *
from sqlalchemy.sql import select, column, table
from sqlalchemy.orm.session import sessionmaker
# from sqlalchemy import DBSession
from datetime import datetime
import pdb

# get the local ip address from LAN
host = get_ip()

session = sessionmaker(autoflush=False)

# declaring our model, here is ORM in its full glory

''' Class Definition Section '''
class Patient(db.Model):
    """
    Used to store all the details of a single patient in an object.
    This class can be used in crud API functions.
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False)
    last_name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), unique=True)
    telephone = db.Column(db.String(10), unique=False)
    address = db.Column(db.String(150), unique=False)

    def __init__(self, first_name, last_name, email, telephone, address):
        """
        This constructor for the Patient class. Assigns all arugments to class
        member variables
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.telephone = telephone
        self.address = address

class PatientSchema(ma.Schema):
    """
    Contains the database schema for the fields used with the Patient class
    """
    class Meta:
        # Fields to expose
        fields = ('first_name', 'last_name', 'email', 'telephone', 'address')

class PatientNotes(db.Model):
    """
    Contains the database schema for the notes fields used within the PatientNotes class
    """

    id = db.Column(db.Integer, primary_key=True)
    
    notes = db.Column(db.String(100), unique=False)
    symptoms = db.Column(db.String(100), unique=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __init__(self, notes, symptoms,patient_id):
        """
        This constructor for the notes class. Assigns all arugments to class
        member variables
        """
        self.notes = notes
        self.symptoms = symptoms
        self.patient_id = patient_id

class PatientNotesSchema(ma.Schema):
    """
    Contains the database schema for the fields used with the Notes class
    """
    class Meta:
        # Fields to expose
        fields = ('notes', 'symptoms','patient_id')

class Doctor(db.Model):
    """
    Used to store all the details of a single doctor in an object.
    This class can be used in crud API functions.
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False)
    last_name = db.Column(db.String(80), unique=False)
    sex = db.Column(db.String(6), unique=False)
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(12), unique=True)
    office = db.Column(db.Integer, unique=False)

    def __init__(self, first_name, last_name, sex, email, phone, office):
        """
        This is the constructor for the Doctor class. Assigns all arugments to class
        member variables
        """
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.email = email
        self.phone = phone
        self.office = office

        
class DoctorSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('first_name', 'last_name', 'sex', 'office', 'email', 'phone')

class Appointment(db.Model):
    """
    Used to store all the details of a single doctor in an object.
    This class can be used in crud API functions.
    """
    ''' create class veriables here '''
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.String(10))
    start_time = db.Column(db.String(8))
    end_time = db.Column(db.String(8))
    description = db.Column(db.String(1024))

    def __init__(self, patient_id, doctor_id, date, start_time, end_time, description):
        """
        This is the constructor for the Appointment class. Assigns all arguments to class
        member variables
        """
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

class AppointmentSchema(ma.Schema):
    """
    Contains the database schema for the fields used with the appointment class
    """
    class Meta:
        # Fields to expose
        fields = ('patient_id', 'doctor_id', 'date', 'start_time', 'end_time', 'description')

''' instantiate objects of each class '''
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)
patient_notes_schema = PatientNotesSchema()
patient_notes_schema = PatientNotesSchema(many=True)
doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)
appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)
''' Crud methods '''

''' Patient Crud '''
# endpoint to create new patient
@app.route("/patient", methods=["POST"])
def add_patient():
    """
    API function used to add a new patient
    """
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    telephone = request.json['telephone']
    address =  request.json['address']

    new_patient = Patient(first_name, last_name, email, telephone, address)

    db.session.add(new_patient)
    db.session.commit()

    print(patient_schema.jsonify(new_patient))

# endpoint to show all patsient
@app.route("/patient", methods=["GET"])
def get_patient():
    """
    API function used to return all of the patients
    """
    all_patients = Patient.query.all()
    result = patients_schema.dump(all_patients)
    return jsonify(result.data)


# endpoint to get patient detail by id
@app.route("/patient/<id>", methods=["GET"])
def patient_detail(id):
    """
    API function used to return a specific patient
    """
    patient = Patient.query.get(id)
    return patient_schema.jsonify(patient)

# endpoint to update patient
@app.route("/patient/<id>", methods=["PUT"])
def patient_update(id):
    """
    API function used to update a specific patient
    """
    patient = Patient.query.get(id)
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    telephone = request.json['telephone']
    address =  request.json['address']

    patient.first_name = first_name
    patient.last_name = last_name
    patient.email = email
    patient.telephone = telephone
    patient.address = address

    db.session.commit()
    return patient_schema.jsonify(patient)

# endpoint to delete patient
@app.route("/patient/<id>", methods=["DELETE"])
def patient_delete(id):
    """
    API function used to delete a specific patient
    """
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()

    return patient_schema.jsonify(patient)

''' Doctor Crud '''
# endpoint to create new doctor
@app.route("/doctor", methods=["POST"])
def add_doctor():
    """
    API function used to add a new doctor
    """
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    sex = request.json['sex']
    email = request.json['email']
    phone = request.json['phone']
    office = request.json['office']

    new_doctor = Doctor(first_name, last_name, sex, email, phone, office)

    db.session.add(new_doctor)
    db.session.commit()

    return doctor_schema.jsonify(new_doctor)

# endpoint to show all doctor
@app.route("/doctor", methods=["GET"])
def get_doctor():
    """
    API function used to return all of the doctors
    """
    all_doctors = Doctor.query.all()
    result = doctors_schema.dump(all_doctors)
    return jsonify(result.data)

# endpoint to get doctor detail by id
@app.route("/doctor/<id>", methods=["GET"])
def doctor_detail(id):
    """
    API function used to return a specific doctor
    """
    doctor = Doctor.query.get(id)
    return doctor_schema.jsonify(doctor)

# endpoint to update doctor
@app.route("/doctor/<id>", methods=["PUT"])
def doctor_update(id):
    """
    API function used to update a specific doctor
    """
    doctor = Doctor.query.get(id)

    ''' add json requests below  fordoctor fields '''
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    sex = request.json['sex']
    email = request.json['email']
    phone = request.json['phone']
    office = request.json['office']

    doctor.first_name = first_name
    doctor.last_name = last_name
    doctor.sex = sex
    doctor.email = email
    doctor.phone = phone
    doctor.office = office

    db.session.commit()
    return doctor_schema.jsonify(doctor)

# endpoint to delete doctor
@app.route("/doctor/<id>", methods=["DELETE"])
def doctor_delete(id):
    """
    API function used to delete a specific doctors
    """
    doctor = Doctor.query.get(id)
    db.session.delete(doctor)
    db.session.commit()

    return doctor_schema.jsonify(doctor)

''' Appointment Crud '''
# endpoint to create new appointment
@app.route("/appointment", methods=["POST"])
def add_appointment():
    """
    API function used to add a new appointment
    """
    patient_id = request.json['patient_id']
    doctor_id = request.json['doctor_id']
    date = request.json['date']
    start_time = request.json['start_time']
    end_time = request.json['end_time']
    description = request.json['description']

    # convert json to python datetime object
    # formatted_start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    # formatted_end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    new_appointment = Appointment(patient_id, doctor_id, date, start_time,
    end_time, description)

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify(new_appointment)

# endpoint to show all apppointments
@app.route("/appointment", methods=["GET"])
def get_appointment():
    """
    API function used to return all of the appointments
    """
    all_appointments = Appointment.query.all()
    result = appointments_schema.dump(all_appointments)
    return jsonify(result.data)

# endpoint to get appointment detail by id
@app.route("/appointment/<id>", methods=["GET"])
def appointment_detail(id):
    """
    API function used to return a specific appointment
    """
    appointment = Appointment.query.get(id)
    return appointment_schema.jsonify(appointment)

# endpoint to update appointment
@app.route("/appointment/<id>", methods=["PUT"])
def appointment_update(id):
    """
    API function used to update a specific appointment
    """
    appointment = request.json['appointment']
    patient_id = request.json['patient_id']
    doctor_id = request.json['doctor_id']
    date = request.json['date']
    start_time = request.json['start_time']
    end_time = request.json['end_time']
    description = request.json['description']

    db.session.commit()
    return appointment_schema.jsonify(appointment)

# endpoint to delete appointment
@app.route("/appointment/<id>", methods=["DELETE"])
def appointment_delete(id):
    """
    API function used to delete a specific appointment
    """
    appointment = Appointment.query.get(id)
    db.session.delete(appointment)
    db.session.commit()

    return appointment_schema.jsonify(appointment)

''' QUERIES '''

# query to return all appointment matchin a patient id
@app.route("/patient-appointment/<id>", methods=["GET"])
def get_appointments_by_patient(id):
    """
    API function used to return all appointments matching a specific patient id
    """

    ''' method 1'''
    appointments = Appointment.query.filter(Appointment.patient_id == id)
    print('Appointments: {}'.format(appointments))

    ''' method 2'''
    # appointments = session.query(Appointment).filter(Appointment.patient_id == id)

    ''' method 3 '''
    # statement = db.select([table('appointment')]).where([column('patient_id') == id])

    # for appointment in appointments:
    #      start_time = appointment.start_time
    #      end_time = appointment.end_time
    #      appointment.start_time = appointment.start_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    #      appointment.end_time = appointment.end_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    #      print('start_time: {}'.format(appointment.start_time))
    #      print('end_time: {}'.format(appointment.end_time))

    # jsonfy the result
    result = appointment_schema.dump(appointments)
    return jsonify(result.data) # returns the result


@app.route("/doctor-appointment/<id>", methods=["GET"])
def get_appointments_by_doctor(id):
    """
    API function used to return all appointments matching a specific doctor id
    """
    statement = db.select([table('appointment')]).where([column('doctor_id') == id])

    # jsonfy the result
    result = appointment_schema.dump(statement)
    return jsonify(result.data) # returns the result

''' Notes Crud '''
# endpoint to create new Notes
@app.route("/notes", methods=["POST"])
def add_note():
    """
    API function used to add a new note
    """
    notes = request.json['notes']
    symptoms = request.json['symptoms']
    patient_id = request.json['patient_id']

    new_note = PatientNotes(notes,symptoms,patient_id)

    db.session.add(new_note)
    db.session.commit()

    print(patient_schema.jsonify(new_note))

#endpoint to show all notes
@app.route("/notes", methods=["GET"])
def get_note():
    """
    API function used to return all of the notes
    """
    all_notes = PatientNotes.query.all()
    result = patient_notes_schema.dump(all_notes)
    return jsonify(result.data)

#endpoint to show a note
@app.route("/notes/<id>", methods=["GET"])
def get_single_note():
    """
    API function used to return single note
    """
    note = PatientNotes.query.get(id)
    return patient_notes_schema.jsonify(note)

#endpoint to get note by id
@app.route("/patient-notes/<id>", methods=["GET"])
def get_notes_by_patient(id):
    """
    API function used to return all Notes matching ID    
    """

    ''' method 1'''
    matchNotes = PatientNotes.query.filter(PatientNotes.patient_id == id)

    # jsonfy the result
    result = PatientNotesSchema.dump(appointments)
    return jsonify(result.data) # returns the result
    
@app.route("/notes/<id>", methods=["PUT"])
def edit_note():
    """
    API function used to add a new note
    """
    notes = request.json['notes']
    symptoms = request.json['symptoms']
    patient_id = request.json['patient_id']

    new_note = PatientNotes(notes,symptoms,patient_id)

    db.session.add(new_note)
    db.session.commit()

    print(patient_schema.jsonify(new_note))
# endpoint to delete note
@app.route("/notes/<id>", methods=["DELETE"])
def note_delete(id):
    """
    API function used to delete a specific notes
    """
    notes = PatientNotes.query.get(id)
    db.session.delete(notes)
    db.session.commit()

    return patient_schema.jsonify(notes)

''' End of Crud Section '''

# start the server
if __name__ == '__main__':
    app.run(host=host, port=5001, debug=False)
