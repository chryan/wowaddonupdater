import logging
import subprocess

def run_cmd(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = process.communicate()
	output = output.decode('ascii').strip()
	error = error.decode('ascii').strip()
	if (len(output) > 0):
		logging.info(output)
	if (len(error) > 0):
		logging.error(error)
