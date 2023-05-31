from sqlalchemy import Column, Integer, String
from database_creation import Base
from Models.Users_Artists import users_artists
from Models.Users_Tracks import users_tracks
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    nickname = Column(String(200))
    spotify_id = Column(String(200))
    is_saved = False


    artists = relationship("Artist", secondary=users_artists, back_populates="users")
    tracks = relationship("Track", secondary=users_tracks, back_populates="users")


    def __init__(self, name, nickname, spotify_id) -> None:
        super().__init__()
        self.name = name
        self.nickname = nickname
        self.spotify_id = spotify_id
        self.is_saved = False

    def __repr__(self) -> str:
        return super().__repr__()
    

