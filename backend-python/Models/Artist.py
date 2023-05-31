from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import mapper, relationship
from database_creation import Base
from Models.Tracks_Artists import tracks_artists
from Models.Users_Artists import users_artists


class Artist(Base):

    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    tracks = relationship("Track", secondary=tracks_artists, back_populates="artists")
    users = relationship("User", secondary=users_artists, back_populates="artists")

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def __repr__(self) -> str:
        return super().__repr__()
    
    

