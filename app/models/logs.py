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
    bs_name = db.StringField(max_length=100)
    fam_name = db.StringField(max_length=100)
    elements = db.ListField(db.IntField())
    bs_fmt = db.StringField(max_length=100)
    ref_fmt = db.StringField(max_length=100)
    help_page = db.StringField(max_length=100)
    user_agent = db.StringField(max_length=256)
    header_email = db.StringField(max_length=100)
    ip_address = db.StringField(max_length=100)
    date = db.DateTimeField(default=datetime.datetime.now)

    meta = {
        'strict': False,     # allow extra fields
        'indexes': [
            "bs_name", "bs_fmt"
        ]
    }

    def __str__(self):
        return 'access:' + str(self.access_type) \
               + ', api: ' + str(self.api) \
               + ', bs_name: ' + str(self.bs_name) \
               + ', fam_name: ' + str(self.fam_name) \
               + ', elements: ' + str(self.elements) \
               + ', bs_fmt: ' + str(self.bs_fmt) \
               + ', ref_fmt: ' + str(self.ref_fmt) \
               + ', help_page: ' + str(self.help_page) \
               + ', user_agent: ' + str(self.user_agent) \
               + ', header_email: ' + str(self.header_email) \
               + ', ip_address: ' + str(self.ip_address) \
               + ', date: ' + str(self.date)


def save_access(access_type, bs_name=None, fam_name=None,
                elements=None, bs_fmt=None, ref_fmt=None,
                help_page=None):

    if not current_app.config['DB_LOGGING']:
        return

    if elements is None:
        elements = []
    else:
        elements = expand_elements(elements)

    ip_address = request.environ.get('REMOTE_ADDR', None)
    user_agent = request.environ.get('HTTP_USER_AGENT', None)
    header_email = request.environ.get('HTTP_FROM', None)

    # Check to see if this was requested directly via the api
    api = request.path.lower().startswith('/api/')

    log = Log(access_type=access_type,
              api=api,
              bs_name=bs_name,
              fam_name=fam_name,
              elements=elements,
              bs_fmt=bs_fmt,
              ref_fmt=ref_fmt,
              help_page=help_page,
              user_agent=user_agent,
              header_email=header_email,
              ip_address=ip_address
              )

    log.save()
