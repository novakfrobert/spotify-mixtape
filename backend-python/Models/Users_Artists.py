from sqlalchemy import Column, Table, ForeignKey
from database_creation import Base

users_artists = Table('users_artists', Base.metadata,
    Column('users_id', ForeignKey('users.id'), primary_key=True),
    Column('artist_id', ForeignKey('artists.id'), primary_key=True)
)