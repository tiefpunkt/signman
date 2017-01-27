from flask import Flask, jsonify, request
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from db import Sign, URL, SignURL
from adminViews import SignView
from config import *

from datetime import datetime

app = Flask(__name__)
app.secret_key = SECRET_KEY

admin = Admin(app, name='SignMan', template_mode='bootstrap3')
admin.add_view(SignView(Sign))
admin.add_view(ModelView(URL))
admin.add_view(ModelView(SignURL))

@app.route('/')
def index():
    return '''<html><body>
    Welcome to Sign Man<p>
    <a href=./admin>Admin interface </a>

    </html></body>
    '''


@app.route('/api/v1/config/<string:token>', methods=['GET'])
def get_config(token):
    lines = []

    try:
        sign = Sign.get(token=token)
        url = sign.getCurrentURL()
        sign.last_ip=request.remote_addr
        sign.save()

    except Sign.DoesNotExist:
        lines.append("# Sign not found")
        url = "%s/nonregistered/%s" % (SIGNMAN_BASE_URL, token)
        if auto_add_signs:
            lines.append("... added to database")
            newSign = Sign(token=token, name="new-%s" % datetime.now().strftime("%Y%m%d-%H%M%S"), last_ip=request.remote_addr)
            newSign.save()

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
    return '''<html><body>
    Connected to SignMan<p>
    Sign Token: %s

    </html></body>''' % token


if __name__ == '__main__':
    app.run(debug=debug)
