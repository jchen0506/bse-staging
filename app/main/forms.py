from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email
from os.path import dirname, join, abspath


def get_choices():
    choices = []
    current_path = dirname(dirname(abspath(__file__)))
    with open(join(current_path, 'static', 'data', 'missing_basis.txt')) as f:
        choices = f.readlines()

    choices = [(c.strip(), c.strip()) for c in choices]
    return choices

class BasisRequestForm(FlaskForm):

    name = StringField('Name')
    email = StringField('Email*', validators=[Email(), DataRequired()])
    requested_basis = SelectField('Requested Basis', choices=get_choices())
    other_basis = StringField('Other basis (not in list)')
    basis_format = StringField('New Basis Set Download Format')
    comments = TextAreaField('Comments')

    # submit = SubmitField('Submit')



