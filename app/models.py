from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin
from datetime import datetime
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

class Ticket(db.Model):


    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)

    def __init__(self):
        self.number = self.id

class Guest(db.Model):

    '''
    A guest is the waiter

        * phonenumber (PK)
        * guest_mac (unique)
        * last_ip
        * last_connected (datetime)
        * request (One To Many)

     '''

    __tablename__ = 'guest'

    id = db.Column(db.Integer, unique=True)
    phone = db.Column(db.String)
    guest_mac = db.Column(db.String)
    # last_ip = 
    request = db.relationship("Request")




class Service(db.Model):

    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    organisation = db.relationship("Organisation", back_populates="service")
    request_type = db.relationship("RequestType")

    # def __str__(self):
    #     return self.name

class Organisation(db.Model):
    ''' Organisation Model '''

    __tablename__ = 'organisation'
    inline_models = (Service,  dict(form_columns=['name']))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    service = db.relationship('Service')

    def __str__(self):
        return self.name

class RequestStatus(db.Model):

    '''
    A status is :
        * order (Integer)
        * title (string (i.e : Being processed, Completed, etc))
        * last_modified_by (many2one -> user_id)
        * last_modified (timestamp)
    '''

    __tablename__ = 'request_status'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

class RequestType(db.Model):
    '''
    RequestType is :

        * title (String, unique)
        * available (Boolean)
        * user_description (String)
        * service_id (many2one -> Service)
    '''
    __tablename__ = 'request_type'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    available = db.Column(db.Boolean)
    user_description = db.Column(db.String)
    # guest_description =
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship("Service", back_populates="request_type")


class Request(db.Model):
    '''
    A request is the reason why a guest is here
        * type_id (many2one -> RequestType)
        * guest_id (many2one -> Guest)
        * status_id (many2one -> Status)
        * timestamp
        unique constraint(type_id, guest_id, status_id)
    '''

    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    rtype_id = db.Column(db.Integer, db.ForeignKey('request_type.id'))
    rtype = db.relationship("RequestType")
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    guest = db.relationship("Guest", back_populates="request")
    status_id = db.Column(db.Integer, db.ForeignKey('request_status.id'))
    status = db.relationship("RequestStatus")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        """Prepare ORM object for serialization"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __str__(self):
        return self.rtype.name + " request #" + self.id
