import datetime
from .. import db
from flask import request


"""
Fields: http://docs.mongoengine.org/apireference.html
mongoengine.fields.

Field Options:
-------------
    db_field: Specify a different field name
    required: Make sure this field is set
    default: Use the given default value if no other value is given
    unique: Make sure no other document in the collection has the same value for this field
    choices: Make sure the field's value is equal to one of the values given in an array
"""


class Log(db.DynamicDocument):     # flexible schema, can have extra attributes

    # added by
    access = db.BooleanField(default=True)
    basis_download = db.BooleanField(default=False)
    basis_set_name = db.StringField(max_length=100)
    elements = db.ListField(db.IntField())
    bs_format = db.StringField(max_length=100)
    date = db.DateTimeField(default=datetime.datetime.now)
    ip_address = db.StringField(max_length=100)

    # Use the $ prefix to set a text index
    meta = {
        # 'allow_inheritance': True,    # known issue with text search
        'strict': False,                # allow extra fields
        'indexes': [
            "basis_set_name", "bs_format"
        ]
    }

    def __unicode__(self):
        return self.basis_set_name

    def __str__(self):
        return 'basis_download:' + self.basis_download + ', basis_set_name: ' \
               + self.basis_set_name + ', bs_format: ' + \
                self.bs_format + ', ip_address: ' + self.ip_address


def save_access(access=True, basis_download=False, basis_set_name=None,
                elements=None, bs_format=None):
    if elements is None:
        elements = []
    log = Log(access=access, basis_download=basis_download,
              ip_address=request.remote_addr,
              basis_set_name=basis_set_name, elements=elements,
              bs_format=bs_format)
    log.save()
