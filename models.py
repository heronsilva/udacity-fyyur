import sys

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy.orm import backref

from enums import DaysOfWeek

db = SQLAlchemy(session_options={"expire_on_commit": False})


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    name = db.Column(db.String)
    phone = db.Column(db.String(120))
    seeking_description = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean, server_default='false')
    state = db.Column(db.String(120))
    website = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @classmethod
    def get(cls, venue_id):
        return cls.query \
            .filter_by(id=venue_id) \
            .join(Show, Show.venue_id == cls.id, isouter=True) \
            .first()

    @classmethod
    def list(cls):
        return cls.query.all()

    @classmethod
    def search(cls, search_term):
        return cls.query \
            .add_columns(Venue.id, Venue.name) \
            .filter(or_(Venue.name.ilike(f'%{search_term}%'),
                        Venue.city.ilike(f'%{search_term}%'),
                        Venue.state.ilike(f'%{search_term}%'))) \
            .all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

            raise
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

            raise
        finally:
            db.session.close()

    @classmethod
    def delete(cls, venue_id):
        try:
            venue = Venue.query.get(venue_id)

            db.session.delete(venue)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

            raise
        finally:
            db.session.close()


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    albums = db.relationship('Album', backref='artist')
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, server_default='false')
    seeking_description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    available_schedules = db.relationship('ArtistSchedule', backref='artist')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

            raise
        finally:
            db.session.close()

    @classmethod
    def get(cls, id):
        return cls.query \
            .filter_by(id=id) \
            .join(Show, Show.artist_id == Artist.id, isouter=True) \
            .first()

    @classmethod
    def list(cls):
        return cls.query.values(Artist.id, Artist.name)

    @classmethod
    def search(cls, search_term):
        return cls.query \
            .join(Show, cls.id == Show.artist_id, isouter=True) \
            .add_columns(cls.id, cls.name) \
            .filter(or_(cls.name.ilike(f'%{search_term}%'),
                        cls.city.ilike(f'%{search_term}%'),
                        cls.state.ilike(f'%{search_term}%'))) \
            .all()

    def update(cls):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

            raise
        finally:
            db.session.close()


class ArtistSchedule(db.Model):
    __tablename__ = 'artist_schedule'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer,
                          db.ForeignKey('artist.id'),
                          nullable=False)
    day_of_week = db.Column(db.Enum(DaysOfWeek,
                                    values_callable=lambda obj: [key.value for key in obj]))
    available = db.Column(db.Boolean(), nullable=False, default=True)
    start_time = db.Column(db.Time, nullable=True, default='09:00:00')
    end_time = db.Column(db.Time, nullable=True, default='23:59:59')


class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    cover = db.Column(db.String, nullable=False)
    songs = db.relationship('Song', backref='album')


class Song(db.Model):
    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    title = db.Column(db.String, nullable=False)


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    artist = db.relationship(
        'Artist',
        cascade='all,delete',
        backref=backref('shows', cascade='all,delete'),
        lazy='joined',
    )
    venue = db.relationship(
        'Venue',
        cascade='all, delete',
        backref=backref('shows', cascade='all,delete'),
        lazy='joined',
    )

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

            raise
        finally:
            db.session.close()

    @classmethod
    def list(cls):
        return Show.query \
            .join(Artist, Artist.id == Show.artist_id) \
            .join(Venue, Venue.id == Show.venue_id)
