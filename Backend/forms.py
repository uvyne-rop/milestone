# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, FileField
from wtforms.validators import DataRequired

class PersonalDetailsForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    contacts = FloatField('Contacts', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    resident_type = StringField('Resident Type', validators=[DataRequired()])
    national_id =  FloatField('National_id', validators=[DataRequired()])
    image = FileField('Image Upload')
