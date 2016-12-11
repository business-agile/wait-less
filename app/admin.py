import os.path as op

from flask import request, Response
from werkzeug.exceptions import HTTPException
from flask_admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask_admin.model.form import InlineFormAdmin

from app import app, db
from app.models import User, Organisation, Service, RequestType, RequestStatus, Guest, Request


admin = Admin(app, name='Admin', template_mode='bootstrap3')

class ModelView(ModelView):

    def is_accessible(self):
        auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            raise HTTPException('', Response('You have to an administrator.', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))
        return True

class GuestView(ModelView):
    form_columns = ('phone', 'guest_mac', 'request')
    column_display_pk = True


# Users
admin.add_view(GuestView(Guest, db.session))
admin.add_view(ModelView(Request, db.session))
admin.add_view(ModelView(RequestType, db.session))
admin.add_view(ModelView(RequestStatus, db.session))
admin.add_view(ModelView(Service, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Organisation, db.session))

