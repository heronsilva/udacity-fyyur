from flask_sqlalchemy import SQLAlchemy

from enums import DaysOfWeek

db = SQLAlchemy()


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

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


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

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


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
        backref='shows',
        lazy='joined',
        cascade='all, delete'
    )
    venue = db.relationship(
        'Venue',
        backref='shows',
        lazy='joined',
        cascade='all, delete'
    )
