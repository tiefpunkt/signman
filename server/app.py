from flask import Flask, jsonify, request, url_for
from flask_admin import Admin
#from flask_admin.contrib.peewee import ModelView
from flask_admin import helpers as admin_helpers
from flask_admin.menu import MenuLink
from flask.ext.security import Security, PeeweeUserDatastore, \
    UserMixin, RoleMixin, login_required, user_registered
from db import Sign, URL, SignURL, User, Role, UserRoles, db
from adminViews import SignView, AuthModelView, AuthAdminIndexView, UserView
from config import *

from datetime import datetime

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_PASSWORD_SALT'] = SECRET_KEY
user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore)

admin = Admin(app, name='SignMan', template_mode='bootstrap3', index_view=AuthAdminIndexView())
admin.add_view(SignView(Sign))
admin.add_view(AuthModelView(URL))
admin.add_view(AuthModelView(SignURL))
admin.add_view(UserView(User))
admin.add_link(MenuLink("Logout", endpoint='security.logout'))

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

@user_registered.connect_via(app)
def activateFirstUser(sender, user, confirm_token, **extra):
    if User.select().count() == 1:
        user.active = True
    else:
        user.active = False

    user.save()
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
