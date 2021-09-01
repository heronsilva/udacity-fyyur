import logging
import sys
from logging import Formatter, FileHandler

import babel
import dateutil.parser
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from sqlalchemy import or_

import config
from enums import DaysOfWeek
from forms import *
from models import db, Artist, Venue, Show, ArtistSchedule

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
moment = Moment(app)
migrate = Migrate(app, db, transaction_per_migration=True)
migrate.init_app(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value

    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    elif format == 'time':
        format = "HH:mm"

    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    recent_artists = Artist.query \
        .order_by(Artist.created_at.desc(), Artist.id.desc()) \
        .limit(10) \
        .all()

    recent_venues = Venue.query \
        .order_by(Venue.created_at.desc(), Venue.id.desc()) \
        .limit(10) \
        .all()

    return render_template('pages/home.html',
                           recent_artists=recent_artists,
                           recent_venues=recent_venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    all_venues = Venue.query.all()
    locations = []
    areas = []

    for venue in all_venues:
        if (venue.city, venue.state) not in locations:
            locations.append((venue.city, venue.state))

    for city, state in locations:
        areas.append({
            "city": city,
            "state": state,
            "venues": list(filter(lambda v: v.city == city, all_venues)),
        })

    return render_template('pages/venues.html', areas=areas)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term')

    data = Venue.query \
        .add_columns(Venue.id, Venue.name) \
        .filter(or_(Venue.name.ilike(f'%{search_term}%'),
                    Venue.city.ilike(f'%{search_term}%'),
                    Venue.state.ilike(f'%{search_term}%'))) \
        .all()

    response = {
        'count': len(data),
        'data': data,
    }

    return render_template('pages/search_venues.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query \
        .filter_by(id=venue_id) \
        .join(Show, Show.venue_id == Venue.id, isouter=True) \
        .first()

    if not venue:
        flash(f"Could not find a venue with the ID #{venue_id}", category='error')
        return redirect(url_for('venues'))

    past_shows_result = list(filter(lambda show: show.start_time <= datetime.now(), venue.shows))
    upcoming_shows_result = list(filter(lambda show: show.start_time >= datetime.now(), venue.shows))
    past_shows = []
    upcoming_shows = []

    for show in past_shows_result:
        past_shows.append({
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time
        })

    for show in upcoming_shows_result:
        upcoming_shows.append({
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time
        })

    data = {
        'id': venue.id,
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'website': venue.website,
        'facebook_link': venue.facebook_link,
        'seeking_talent': venue.seeking_talent,
        'image_link': venue.image_link,
        'past_shows': past_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows': upcoming_shows,
        'upcoming_shows_count': len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    return render_template('forms/new_venue.html', form=VenueForm())


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form, meta={'csrf': False})

    if request.method == 'POST' and form.validate():
        try:
            venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                image_link=form.image_link.data or None,
                facebook_link=form.facebook_link.data or None,
                genres=form.genres.data,
                website=form.website_link.data or None,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data or None,
            )

            db.session.add(venue)
            db.session.commit()

            flash('Venue ' + venue.name + ' was successfully listed!')
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Venue ' + form.name.data + ' could not be listed.', category='error')
        finally:
            db.session.close()

        return render_template('pages/home.html')
    else:
        errors = []

        for field, error in form.errors.items():
            errors.append(f'{field}: {error}')

        flash(f'Request errors {str(errors)}', category='error')

        return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)

        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash(f'An error occurred. Could not delete venue with ID #{venue_id}')
    finally:
        db.session.close()

    return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = Artist.query.values(Artist.id, Artist.name)
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term')

    data = Artist.query \
        .join(Show, Artist.id == Show.artist_id) \
        .add_columns(Artist.id, Artist.name) \
        .filter(or_(Artist.name.ilike(f'%{search_term}%'),
                    Artist.city.ilike(f'%{search_term}%'),
                    Artist.state.ilike(f'%{search_term}%'))) \
        .all()

    response = {
        'count': len(data),
        'data': data,
    }

    return render_template('pages/search_artists.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query \
        .filter_by(id=artist_id) \
        .join(Show, Show.artist_id == Artist.id, isouter=True) \
        .first()

    if not artist:
        flash(f"Could not find an artist with the ID #{artist_id}", category='error')
        return redirect(url_for('artists'))

    past_shows_result = list(filter(lambda show: show.start_time <= datetime.now(), artist.shows))
    upcoming_shows_result = list(filter(lambda show: show.start_time >= datetime.now(), artist.shows))
    past_shows = []
    upcoming_shows = []

    for show in past_shows_result:
        past_shows.append({
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time,
        })

    for show in upcoming_shows_result:
        upcoming_shows.append({
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time,
        })

    data = {
        'id': artist.id,
        'name': artist.name,
        'genres': artist.genres,
        'albums': artist.albums,
        'albums_count': len(artist.albums),
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'seeking_venue': artist.seeking_venue,
        'seeking_description': artist.seeking_description,
        'image_link': artist.image_link,
        'facebook_link': artist.facebook_link,
        'website': artist.website,
        'past_shows': past_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows': upcoming_shows,
        'upcoming_shows_count': len(upcoming_shows),
        'available_schedules': artist.available_schedules,
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query \
        .filter_by(id=artist_id) \
        .join(Show, Show.artist_id == Artist.id, isouter=True) \
        .first()

    form = ArtistForm(obj=artist)

    return render_template('forms/edit_artist.html',
                           form=form,
                           artist=artist,
                           days_of_week=DaysOfWeek)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form, meta={'csrf': False})

    if request.method == 'POST' and form.validate():
        try:
            artist = Artist.query.get(artist_id)
            artist.name = form.name.data
            artist.city = form.city.data
            artist.facebook_link = form.facebook_link.data
            artist.image_link = form.image_link.data
            artist.genres = form.genres.data
            artist.phone = form.phone.data
            artist.website = form.website_link.data
            artist.state = form.state.data
            artist.seeking_venue = form.seeking_venue.data
            artist.seeking_description = form.seeking_description.data

            for schedule in artist.available_schedules:
                day_of_week = schedule.day_of_week.name
                available = request.form.get(day_of_week) == 'on' and form.seeking_venue.data

                schedule.available = available
                schedule.start_time = request.form.get(f'{day_of_week}_schedule_start_time') if available else None
                schedule.end_time = request.form.get(f'{day_of_week}_schedule_end_time') if available else None

            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash(f'An error occurred. Artist {artist_id} could not be updated.', category='error')
        finally:
            db.session.close()

        return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        errors = []

        for field, error in form.errors.items():
            errors.append(f'{field}: {error}')

        flash(f'Request errors {str(errors)}', category='error')

        return redirect(url_for('edit_artist'))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(obj=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form, meta={'csrf': False})

    if request.method == 'POST' and form.validate():
        try:
            venue = Venue.query.get(venue_id)
            venue.name = form.name.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.address = form.address.data
            venue.phone = form.phone.data
            venue.image_link = form.image_link.data or None
            venue.facebook_link = form.facebook_link.data or None
            venue.genres = form.genres.data
            venue.website = form.website_link.data or None
            venue.seeking_talent = form.seeking_talent.data
            venue.seeking_description = form.seeking_description.data or None

            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        return redirect(url_for('show_venue', venue_id=venue_id))
    else:
        errors = []

        for field, error in form.errors.items():
            errors.append(f'{field}: {error}')

        flash(f'Request errors {str(errors)}', category='error')

        return redirect(url_for('create_artist_form'))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    return render_template('forms/new_artist.html',
                           form=ArtistForm(),
                           days_of_week=DaysOfWeek)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form, meta={'csrf': False})

    if request.method == 'POST' and form.validate():
        try:
            artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=form.genres.data,
                image_link=form.image_link.data or None,
                facebook_link=form.facebook_link.data or None,
                website=form.website_link.data or None,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data or None,
            )

            for day in list(DaysOfWeek):
                selected = request.form.get(f'{day}') == 'on'

                if selected:
                    artist.available_schedules.append(
                        ArtistSchedule(
                            day_of_week=day.value,
                            start_time=request.form.get(f'{day}_schedule_start_time'),
                            end_time=request.form.get(f'{day}_schedule_end_time')
                        )
                    )

            db.session.add(artist)
            db.session.commit()

            flash('Artist ' + artist.name + ' was successfully listed!')
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.', category='error')
        finally:
            db.session.close()

        return redirect(url_for('index'))
    else:
        errors = []

        for field, error in form.errors.items():
            errors.append(f'{field}: {error}')

        flash(f'Request errors {str(errors)}', category='error')

        return redirect(url_for('create_artist_form'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    result = Show.query.join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id)
    data = []

    for show in result:
        data.append({
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time,
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    return render_template('forms/new_show.html', form=ShowForm())


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form, meta={'csrf': False})

    if request.method == 'POST' and form.validate():
        try:
            show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                name=form.name.data,
                start_time=form.start_time
            )

            start_time = datetime.fromisoformat(show.start_time).time()
            day_of_week = datetime.fromisoformat(show.start_time).strftime('%A')

            artist_schedules = ArtistSchedule.query \
                .filter(ArtistSchedule.artist_id == show.artist_id,
                        ArtistSchedule.day_of_week == day_of_week,
                        ArtistSchedule.start_time <= start_time,
                        ArtistSchedule.end_time >= start_time) \
                .all()

            if not artist_schedules:
                flash('This artist is not available during the specified time', category='error')
                return render_template('forms/new_show.html', form=form)

            db.session.add(show)
            db.session.commit()

            flash('Show was successfully listed!')
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Show could not be listed', category='error')
        finally:
            db.session.close()

        return redirect(url_for('index'))
    else:
        errors = []

        for field, error in form.errors.items():
            errors.append(f'{field}: {error}')

        flash(f'Request errors {str(errors)}', category='error')

        return redirect(url_for('create_shows'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run()
