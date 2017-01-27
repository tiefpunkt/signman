from flask_admin.contrib.peewee import ModelView
from db import SignURL


class SignView(ModelView):
    column_list = ('name', 'token', 'last_ip')
    form_excluded_columns = ['last_ip', 'last_url', 'last_url_first_send']

    inline_models = (SignURL,)
