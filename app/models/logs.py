import datetime
from .. import db
from flask import request


class Log(db.DynamicDocument):   # flexible schema, can have extra attributes
    """
    Stores searches and downloads of basis sets by users.
    Each Log is an access to specific basis set, basis format, and optionally
    list of elements.

    Attributes
    ----------
    download : bool
        if this access is a download request
    bs_name: str
        Basis set name
    bs_format: str
        Basis set format
    ip_address: str
        IP address of the cclient requesting the basis set
    date: datetime
        date of the search/download in the server local time

    """

    download = db.BooleanField()
    bs_name = db.StringField(max_length=100)
    elements = db.ListField(db.IntField())
    bs_format = db.StringField(max_length=100)
    date = db.DateTimeField(default=datetime.datetime.now)
    ip_address = db.StringField(max_length=100)
    comment = db.StringField(max_length=100)

    meta = {
        'strict': False,     # allow extra fields
        'indexes': [
            "bs_name", "bs_format"
        ]
    }

    def __str__(self):
        return 'Download:' + str(self.download) \
               + ', basis_set_name: ' + str(self.bs_name) \
               + ', bs_format: ' + str(self.bs_format) \
               + ', IP_address: ' + str(self.ip_address)


def save_access(download=False, bs_name=None,
                elements=None, bs_format=None):

    if elements is None:
        elements = []

    ip_address = request.environ.get('REMOTE_ADDR', None)

    log = Log(download=download,
              ip_address=ip_address,
              bs_name=bs_name, elements=elements,
              bs_format=bs_format)

    log.save()
