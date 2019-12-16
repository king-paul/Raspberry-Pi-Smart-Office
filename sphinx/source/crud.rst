CRUD API
========
This page contains all the classes and functions found with the crud module. This file can be found in root/curd/crud.py

.. automodule:: crud

Patient Crud
------------
.. autoclass:: Patient
    :members:

    .. autoclass:: PatientSchema
        :members:

    .. autofunction:: add_patient
    .. autofunction:: get_patient
    .. autofunction:: patient_detail
    .. autofunction:: patient_update
    .. autofunction:: patient_delete


Doctor Crud
-----------
.. autoclass:: Doctor
    :members:

    .. autoclass:: DoctorSchema
        :members:

    .. autofunction:: add_doctor
    .. autofunction:: get_doctor
    .. autofunction:: doctor_detail
    .. autofunction:: doctor_update
    .. autofunction:: doctor_delete

Appointment Crud
----------------
.. autoclass:: Appointment
    :members:

    .. autoclass:: AppointmentSchema
        :members:

    .. autofunction:: add_appointment
    .. autofunction:: get_appointment
    .. autofunction:: appointment_detail
    .. autofunction:: appointment_update
    .. autofunction:: appointment_delete

Queries
-------
.. autofunction:: get_appointments_by_patient
.. autofunction:: get_appointments_by_doctor