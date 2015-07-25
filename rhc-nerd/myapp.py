from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"


import os
ip = os.environ['OPENSHIFT_PYTHON_IP']
port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
host_name = os.environ['OPENSHIFT_GEAR_DNS']

if __name__ == "__main__":
	app.run(host_name, int(port))
