from sqlalchemy import Column, Table, ForeignKey
from database_creation import Base

tracks_artists = Table('tracks_artists', Base.metadata,
    Column('track_id', ForeignKey('tracks.id'), primary_key=True),
    Column('artist_id', ForeignKey('artists.id'), primary_key=True)
)