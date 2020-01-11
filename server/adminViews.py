from flask_admin.contrib.peewee import ModelView
from flask_admin import AdminIndexView, expose
from flask_security import current_user
from flask import redirect, url_for,request
from db import SignURL

# Create customized model view class
class AuthModelView(ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

      #  if current_user.has_role('superuser'):
      #      return True

        return True

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            # permission denied
            abort(403)
        else:
            # login
            return redirect(url_for('security.login', next=request.url))

class AuthAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return redirect(url_for('security.login', next=request.url))
        else:
            return self.render(self._template)

class SignView(AuthModelView):
    column_list = ('name', 'token', 'last_ip')
    form_excluded_columns = ['last_ip', 'last_url', 'last_url_first_send']

    inline_models = (SignURL,)

class UserView(AuthModelView):
    column_exclude_list = ['password', ]
    column_editable_list = ['active']
    form_excluded_columns = ['password']
    can_create = False
