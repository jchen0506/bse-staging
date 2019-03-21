import datetime
from .. import db
from flask import request, current_app
from basis_set_exchange.misc import expand_elements


class Log(db.DynamicDocument):   # flexible schema, can have extra attributes
    """
    Stores searches and downloads of basis sets by users.
    Each Log is an access to specific basis set, basis format, and optionally
    list of elements.

    Attributes
    ----------
    download : bool
        if this access is a download request
    name: str
        Basis set name
    fmt: str
        Basis set format
    ip_address: str
        IP address of the cclient requesting the basis set
    date: datetime
        date of the search/download in the server local time

    """

    access_type = db.StringField(max_length=32)
    api = db.BooleanField()
    basis_name = db.StringField(max_length=100)
    basis_version = db.StringField(max_length=10)
    family_name = db.StringField(max_length=100)
    elements = db.ListField(db.IntField())
    basis_format = db.StringField(max_length=100)
    reference_format = db.StringField(max_length=100)
    help_page = db.StringField(max_length=100)
    user_agent = db.StringField(max_length=256)
    header_email = db.StringField(max_length=100)
    ip_address = db.StringField(max_length=100)
    referrer = db.StringField(max_length=256)
    uncontract_general = db.BooleanField(default=False)
    uncontract_segmented = db.BooleanField(default=False)
    uncontract_spdf = db.BooleanField(default=False)
    optimize_general = db.BooleanField(default=False)
    make_general = db.BooleanField(default=False)
    date = db.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'strict': False,     # allow extra fields
        'indexes': [
            "basis_name", "basis_format"
        ]
    }

    def __str__(self):
        return 'access: ' + str(self.access_type) \
               + ', api: ' + str(self.api) \
               + ', basis_name: ' + str(self.basis_name) \
               + ', basis_version: ' + str(self.basis_version) \
               + ', family_name: ' + str(self.family_name) \
               + ', elements: ' + str(self.elements) \
               + ', basis_format: ' + str(self.basis_format) \
               + ', reference_format: ' + str(self.reference_format) \
               + ', help_page: ' + str(self.help_page) \
               + ', user_agent: ' + str(self.user_agent) \
               + ', header_email: ' + str(self.header_email) \
               + ', ip_address: ' + str(self.ip_address) \
               + ', referrer: ' + str(self.referrer) \
               + ', uncontract_general: ' + str(self.uncontract_general) \
               + ', uncontract_segmented: ' + str(self.uncontract_segmented) \
               + ', uncontract_spdf: ' + str(self.uncontract_spdf) \
               + ', make_general: ' + str(self.make_general) \
               + ', optimize_general: ' + str(self.optimize_general) \
               + ', date: ' + str(self.date)


def save_access(access_type, **kwargs):

    if not current_app.config['DB_LOGGING']:
        return

    if 'elements' in kwargs:
        kwargs['elements'] = expand_elements(kwargs['elements'])

    # The IP address is the last address listed in access_route, which
    # comes from the X-FORWARDED-FOR header
    # (If access_route is empty, use the original request ip)
    if len(request.access_route) > 0:
        ip_address = request.access_route[-1]
    else:
        ip_address = request.remote_addr

    user_agent = request.environ.get('HTTP_USER_AGENT', None)
    header_email = request.environ.get('HTTP_FROM', None)
    referrer = request.referrer

    # Check to see if this was requested directly via the api
    api = request.path.lower().startswith('/api/')

    log = Log(access_type=access_type,
              api=api,
              ip_address=ip_address,
              user_agent=user_agent,
              header_email=header_email,
              referrer=referrer,
              **kwargs)

    log.save()
