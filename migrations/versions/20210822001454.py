"""Populate artist albums and songs

Revision ID: a58cebf54a72
Revises: 49625c006a91
Create Date: 2021-08-22 00:14:54.247966

"""
import random

from alembic import op
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import SQLALCHEMY_DATABASE_URI
from models import Album, Song

# revision identifiers, used by Alembic.
revision = 'a58cebf54a72'
down_revision = '49625c006a91'
branch_labels = None
depends_on = '49625c006a91'

fake = Faker()
engine = create_engine(SQLALCHEMY_DATABASE_URI)


def upgrade():
    with Session(engine) as session:
        for i in range(300):
            album = Album(
                artist_id=random.choice(list(range(1, 100))),
                title=fake.text(max_nb_chars=20),
                cover='https://source.unsplash.com/400x600/?music',
            )

            for j in range(random.choice(list(range(5, 15)))):
                album.songs.append(Song(
                    album_id=album.id,
                    title=fake.text(max_nb_chars=20),
                ))

            session.add(album)
            session.commit()


def downgrade():
    op.execute('TRUNCATE TABLE album, song RESTART IDENTITY CASCADE;')
