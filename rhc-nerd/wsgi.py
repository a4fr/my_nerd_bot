import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
	exec_namespace = dict(__file__=virtualenv)
	with open(virtualenv, 'rb') as exec_file:
		file_contents = exec_file.read()
	compiled_code = compile(file_contents, virtualenv, 'exec')
	exec(compiled_code, exec_namespace)
except IOError:
 	pass
  
  
from nerd_reporter import app as application
#from myapp import app as application
