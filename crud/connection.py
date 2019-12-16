"""
This file contains the database connection information which is used by the crud API
"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os, sys, subprocess

def get_ip():
	ip = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
	array = ip.split(' ')
	return array[0]

# get the host from the comment line argument if there is one
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

''' This is the connection information'''
USER   = 'root'
PASS   = 'pkgJw4aIB32i73aE'
HOST   = '35.189.27.220'
DBNAME = 'crudDB'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/crud'.format(USER,PASS,HOST,DBNAME)
db = SQLAlchemy(app)
ma = Marshmallow(app)