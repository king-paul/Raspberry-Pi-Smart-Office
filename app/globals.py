from app import app
import subprocess

# returns the lan ip address in ipv4 format
def get_ip():
	"""
	Returns the local IP (LAN) address of the device the Flask web server is running on
	"""
	ip = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
	array = ip.split(' ')
	return array[0]