from .. import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BasisRequest(db.Document):
    """Request done by users"""

    name = db.StringField()
    email = db.EmailField(max_length=128)
    requested_basis = db.StringField()
    other_basis = db.StringField(max_length=128)
    comments = db.StringField()
    date = db.DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': [
            'requested_basis',
        ]
    }



