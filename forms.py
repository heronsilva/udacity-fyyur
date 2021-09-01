from datetime import timedelta, datetime

from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL, Regexp, Optional

from enums import Genre


class ShowForm(Form):
    name = StringField('show_name')
    artist_id = StringField('artist_id')
    venue_id = StringField('venue_id')
    start_time = DateTimeField('start_time',
                               validators=[DataRequired()],
                               default=datetime.today() + timedelta(days=1))


class VenueForm(Form):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state',
                        validators=[DataRequired()],
                        choices=[
                            ('AL', 'AL'),
                            ('AK', 'AK'),
                            ('AZ', 'AZ'),
                            ('AR', 'AR'),
                            ('CA', 'CA'),
                            ('CO', 'CO'),
                            ('CT', 'CT'),
                            ('DE', 'DE'),
                            ('DC', 'DC'),
                            ('FL', 'FL'),
                            ('GA', 'GA'),
                            ('HI', 'HI'),
                            ('ID', 'ID'),
                            ('IL', 'IL'),
                            ('IN', 'IN'),
                            ('IA', 'IA'),
                            ('KS', 'KS'),
                            ('KY', 'KY'),
                            ('LA', 'LA'),
                            ('ME', 'ME'),
                            ('MT', 'MT'),
                            ('NE', 'NE'),
                            ('NV', 'NV'),
                            ('NH', 'NH'),
                            ('NJ', 'NJ'),
                            ('NM', 'NM'),
                            ('NY', 'NY'),
                            ('NC', 'NC'),
                            ('ND', 'ND'),
                            ('OH', 'OH'),
                            ('OK', 'OK'),
                            ('OR', 'OR'),
                            ('MD', 'MD'),
                            ('MA', 'MA'),
                            ('MI', 'MI'),
                            ('MN', 'MN'),
                            ('MS', 'MS'),
                            ('MO', 'MO'),
                            ('PA', 'PA'),
                            ('RI', 'RI'),
                            ('SC', 'SC'),
                            ('SD', 'SD'),
                            ('TN', 'TN'),
                            ('TX', 'TX'),
                            ('UT', 'UT'),
                            ('VT', 'VT'),
                            ('VA', 'VA'),
                            ('WA', 'WA'),
                            ('WV', 'WV'),
                            ('WI', 'WI'),
                            ('WY', 'WY'),
                        ])
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(), Regexp(r'\d{3}-\d{3}-\d{4}')])
    image_link = StringField('image_link')
    genres = SelectMultipleField('genres',
                                 validators=[DataRequired()],
                                 choices=Genre.options())
    facebook_link = StringField('facebook_link', validators=[Optional(), URL()])
    website_link = StringField('website_link')
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = StringField('seeking_description')


class ArtistForm(Form):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state',
                        validators=[DataRequired()],
                        choices=[
                            ('AL', 'AL'),
                            ('AK', 'AK'),
                            ('AZ', 'AZ'),
                            ('AR', 'AR'),
                            ('CA', 'CA'),
                            ('CO', 'CO'),
                            ('CT', 'CT'),
                            ('DE', 'DE'),
                            ('DC', 'DC'),
                            ('FL', 'FL'),
                            ('GA', 'GA'),
                            ('HI', 'HI'),
                            ('ID', 'ID'),
                            ('IL', 'IL'),
                            ('IN', 'IN'),
                            ('IA', 'IA'),
                            ('KS', 'KS'),
                            ('KY', 'KY'),
                            ('LA', 'LA'),
                            ('ME', 'ME'),
                            ('MT', 'MT'),
                            ('NE', 'NE'),
                            ('NV', 'NV'),
                            ('NH', 'NH'),
                            ('NJ', 'NJ'),
                            ('NM', 'NM'),
                            ('NY', 'NY'),
                            ('NC', 'NC'),
                            ('ND', 'ND'),
                            ('OH', 'OH'),
                            ('OK', 'OK'),
                            ('OR', 'OR'),
                            ('MD', 'MD'),
                            ('MA', 'MA'),
                            ('MI', 'MI'),
                            ('MN', 'MN'),
                            ('MS', 'MS'),
                            ('MO', 'MO'),
                            ('PA', 'PA'),
                            ('RI', 'RI'),
                            ('SC', 'SC'),
                            ('SD', 'SD'),
                            ('TN', 'TN'),
                            ('TX', 'TX'),
                            ('UT', 'UT'),
                            ('VT', 'VT'),
                            ('VA', 'VA'),
                            ('WA', 'WA'),
                            ('WV', 'WV'),
                            ('WI', 'WI'),
                            ('WY', 'WY'),
                        ])
    phone = StringField('phone', validators=[DataRequired(), Regexp(r'\d{3}-\d{3}-\d{4}')])
    image_link = StringField('image_link')
    genres = SelectMultipleField('genres',
                                 validators=[DataRequired()],
                                 choices=Genre.options())
    facebook_link = StringField('facebook_link', validators=[Optional(), URL()])
    website_link = StringField('website_link')
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = StringField('seeking_description')
