"""Setup tables

Revision ID: e4ec480e9e4a
Revises: 
Create Date: 2021-08-21 19:13:41.168282

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e4ec480e9e4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('artist',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('genres', sa.ARRAY(sa.String()), nullable=True),
                    sa.Column('city', sa.String(length=120), nullable=True),
                    sa.Column('state', sa.String(length=120), nullable=True),
                    sa.Column('phone', sa.String(length=120), nullable=True),
                    sa.Column('website', sa.String(length=120), nullable=True),
                    sa.Column('image_link', sa.String(length=500), nullable=True),
                    sa.Column('facebook_link', sa.String(length=120), nullable=True),
                    sa.Column('seeking_venue', sa.Boolean(), server_default='false', nullable=True),
                    sa.Column('seeking_description', sa.String(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('venue',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('address', sa.String(length=120), nullable=True),
                    sa.Column('city', sa.String(length=120), nullable=True),
                    sa.Column('facebook_link', sa.String(length=120), nullable=True),
                    sa.Column('genres', sa.ARRAY(sa.String()), nullable=True),
                    sa.Column('image_link', sa.String(length=500), nullable=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('phone', sa.String(length=120), nullable=True),
                    sa.Column('seeking_description', sa.String(), nullable=True),
                    sa.Column('seeking_talent', sa.Boolean(), server_default='false', nullable=True),
                    sa.Column('state', sa.String(length=120), nullable=True),
                    sa.Column('website', sa.String(length=120), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('album',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('artist_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('cover', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('artist_schedule',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('artist_id', sa.Integer(), nullable=False),
                    sa.Column('start_time', sa.Time(), nullable=True, default='00:00:00'),
                    sa.Column('end_time', sa.Time(), nullable=True, default='23:59:59'),
                    sa.Column('day_of_week',
                              sa.Enum('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
                                      name='days_of_week'),
                              nullable=False),
                    sa.Column('available', sa.Boolean(), nullable=False, server_default='true'),
                    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('artist_id', 'day_of_week', )
                    )
    op.create_table('show',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('artist_id', sa.Integer(), nullable=False),
                    sa.Column('venue_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('start_time', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
                    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('song',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('album_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('song')
    op.drop_table('show')
    op.drop_table('artist_schedule')
    op.drop_table('album')
    op.drop_table('venue')
    op.drop_table('artist')
    op.execute('DROP TYPE days_of_week;')
