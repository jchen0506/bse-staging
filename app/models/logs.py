import datetime
from .. import db
from flask import request


class Log(db.DynamicDocument):   # flexible schema, can have extra attributes

    access = db.BooleanField(default=True)
    download = db.BooleanField(default=False)
    bs_name = db.StringField(max_length=100)
    elements = db.ListField(db.IntField())
    bs_format = db.StringField(max_length=100)
    date = db.DateTimeField(default=datetime.datetime.now)
    ip_address = db.StringField(max_length=100)

    meta = {
        'strict': False,     # allow extra fields
        'indexes': [
            "bs_name", "bs_format"
        ]
    }

    def __unicode__(self):
        return self.bs_name

    def __str__(self):
        return 'Download:' + self.download + ', basis_set_name: ' \
               + self.bs_name + ', bs_format: ' + \
                self.bs_format + ', IP_address: ' + self.ip_address


def save_access(access=True, download=False, bs_name=None,
                elements=None, bs_format=None):

    if elements is None:
        elements = []

    try:
        ip_address = ip_address = request.environ['REMOTE_ADDR']
    except:
        ip_address = None

    log = Log(access=access, download=download,
              ip_address=ip_address,
              bs_name=bs_name, elements=elements,
              bs_format=bs_format)

    log.save()
