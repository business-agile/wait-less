from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin

from app import db, bcrypt

class User(db.Model, UserMixin):

    ''' A user who has an account on the website. '''

    __tablename__ = 'users'

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    confirmation = db.Column(db.Boolean)
    _password = db.Column(db.String)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        return self.email


class Queue(db.Model):
    ''' A queue is the represention of the waiting line '''

    __tablename__ = 'queue'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship("Service", back_populates="queue")
    



class Service(db.Model):

    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    organisation = db.relationship("Organisation", back_populates="service")
    queue = db.relationship("Queue")

    def __str__(self):
        return self.name

class Organisation(db.Model):
    ''' Organisation Model '''

    __tablename__ = 'organisation'
    inline_models = (Service,  dict(form_columns=['name']))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    service = db.relationship('Service')

    def __str__(self):
        return self.name
