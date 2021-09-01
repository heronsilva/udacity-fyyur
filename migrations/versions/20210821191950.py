"""Populate Artists, Venues and Shows

Revision ID: 49625c006a91
Revises: e4ec480e9e4a
Create Date: 2021-08-21 19:19:50.405843

"""
import random
from datetime import datetime, timedelta

from alembic import op
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import Artist, Venue, Show, ArtistSchedule
from config import SQLALCHEMY_DATABASE_URI
from enums import DaysOfWeek

# revision identifiers, used by Alembic.
revision = '49625c006a91'
down_revision = 'e4ec480e9e4a'
branch_labels = None
depends_on = 'e4ec480e9e4a'

fake = Faker()
engine = create_engine(SQLALCHEMY_DATABASE_URI)

artists = []
venues = []

genres = [
    'Alternative',
    'Blues',
    'Classical',
    'Country',
    'Electronic',
    'Folk',
    'Funk',
    'Hip-Hop',
    'Heavy Metal',
    'Instrumental',
    'Jazz',
    'Musical Theatre',
    'Pop',
    'Punk',
    'R&B',
    'Reggae',
    'Rock n Roll',
    'Soul',
    'Other',
]

states = [
    'AL',
    'AK',
    'AZ',
    'AR',
    'CA',
    'CO',
    'CT',
    'DE',
    'DC',
    'FL',
    'GA',
    'HI',
    'ID',
    'IL',
    'IN',
    'IA',
    'KS',
    'KY',
    'LA',
    'ME',
    'MT',
    'NE',
    'NV',
    'NH',
    'NJ',
    'NM',
    'NY',
    'NC',
    'ND',
    'OH',
    'OK',
    'OR',
    'MD',
    'MA',
    'MI',
    'MN',
    'MS',
    'MO',
    'PA',
    'RI',
    'SC',
    'SD',
    'TN',
    'TX',
    'UT',
    'VT',
    'VA',
    'WA',
    'WV',
    'WI',
    'WY',
]


def upgrade():
    with Session(engine) as session:
        #  Generate artists
        for artist_id in range(100):
            seeking_venue = fake.boolean()

            artist = Artist(
                name='[A] ' + fake.name(),
                city=fake.city(),
                state=random.choice(states),
                phone=fake.numerify('###-###-####'),
                genres=random.choices(genres, k=random.choice([1, 2, 3])),
                website=fake.hostname(),
                image_link='https://source.unsplash.com/300x200/?singer',
                facebook_link='https://www.facebook.com/' + fake.user_name(),
                seeking_venue=seeking_venue,
                seeking_description=fake.sentence() if seeking_venue else None
            )

            # Generate the artist's available schedules
            for day in DaysOfWeek:
                available = fake.boolean()

                min_datetime = datetime.now().replace(hour=9, minute=0, second=0)
                max_datetime = datetime.now().replace(hour=23, minute=59, second=59)

                start_date = fake.date_time_between_dates(min_datetime, max_datetime)
                end_date = fake.date_time_between_dates(start_date, max_datetime)

                artist.available_schedules.append(
                    ArtistSchedule(
                        artist_id=artist.id,
                        day_of_week=day.value,
                        available=available,
                        start_time=start_date.time().replace(second=0) if available else None,
                        end_time=end_date.time().replace(second=0) if available else None,
                    )
                )

            artists.append(artist)
            session.add(artist)

        for venue_id in range(30):
            venue = Venue(
                name='[V] ' + fake.company(),
                address=fake.address(),
                city=fake.city(),
                facebook_link='https://www.facebook.com/' + fake.user_name(),
                genres=random.choices(genres, k=random.choice([1, 2, 3])),
                image_link='https://source.unsplash.com/400x600/?concert',
                phone=fake.phone_number(),
                seeking_description=fake.catch_phrase(),
                seeking_talent=fake.boolean(),
                state=random.choice(states),
                website=fake.hostname()
            )
            venues.append(venue)
            session.add(venue)

        for show_id in range(300):
            session.add(Show(
                name='[S] ' + fake.text(),
                artist=random.choice(artists),
                venue=random.choice(venues),
                start_time=datetime.today() + timedelta(days=random.randrange(-100, 100))
            ))

        session.commit()


def downgrade():
    op.execute('TRUNCATE TABLE artist, venue RESTART IDENTITY CASCADE;')
