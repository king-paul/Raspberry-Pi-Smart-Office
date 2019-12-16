.. Medical Appointment System (MAPS) documentation master file, created by
   sphinx-quickstart on Sun Oct 14 13:20:40 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Medical Appointment System (MAPS)'s documentation!
=============================================================
This is a documentation written using Sphinx for Assignment 2 of Programming the Internet of things.

About this Project
------------------
Maps is a an automated doctor's appoitment scheduling suystem made for a medical office in Melbourne to replace the process that is usually handled by recptionists.

This application uses a Python Flask based webstie designed to run on the Raspberry Pi. it also reads and writes data to and SQL database located on Google Cloud using CloudSQL.

Requirements
------------
A Raspberry Pi Model B with an installation of Rasbian is needed to run start this application. You also need to have Python 3 or later installed along with the packages listed in the requirements.txt file.

Contents:

.. toctree::
   :maxdepth: 2
   
   routes
   crud
   forms
   globals

..   :caption: Contents:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
