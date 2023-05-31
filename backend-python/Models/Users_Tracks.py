from sqlalchemy import Column, Table, ForeignKey
from database_creation import Base

users_tracks = Table('users_tracks', Base.metadata,
    Column('track_id', ForeignKey('tracks.id'), primary_key=True),
    Column('users_id', ForeignKey('users.id'), primary_key=True)
)