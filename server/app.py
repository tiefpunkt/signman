from flask import Flask, jsonify
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from db import Sign, URL, SignURL
from adminViews import SignView

app = Flask(__name__)
app.secret_key = "osYJNVBIAZVBSKHBSLKFWbeiubkBLHBU3IBIHFBPI"

admin = Admin(app, name='SignMan', template_mode='bootstrap3')
admin.add_view(SignView(Sign))
admin.add_view(ModelView(URL))
admin.add_view(ModelView(SignURL))

DEFAULT_URL = "http://status.munichmakerlab.de"

@app.route('/')
def index():
	return "Sign Man\n"

@app.route('/api/v1/config/<string:token>', methods=['GET'])
def get_config(token):
	lines = []

	try:
		sign = Sign.get(token=token)
		url = sign.getCurrentURL()
	except Sign.DoesNotExist:
		lines.append("# Sign not found")
		# url = DEFAULT_URL
		url = "http://signman.intern.munichmakerlab.de/nonregistered/%s" % token 
	except URL.DoesNotExist:
		lines.append("# No URL for sign found")
		url = DEFAULT_URL

	lines.append("URL %s" % url)
	lines.append("NODE %s" % token)
	lines.append("")
	return "\n".join(lines)

@app.route('/api/v1/sign/<string:token>', methods=['GET'])
def get_urls(token):
	try:
		sign = Sign.get(token=token)
	except:
		return "sign not found"
	return jsonify(sign.activeURLs())

@app.route('/nonregistered/<string:token>', methods=['GET'])
def non_registered_screen(token):
	return "<html><body>Connected to SignMan<br>Sign not registered<br>Sign Token: %s" % token

if __name__ == '__main__':
	app.run(debug=True)
