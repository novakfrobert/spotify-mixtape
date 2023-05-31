from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapper, relationship
from database_creation import Base
from Models.Tracks_Artists import tracks_artists
from Models.Users_Tracks import users_tracks


class Track(Base):

    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    uri = Column(String(200))

    artists = relationship("Artist", secondary=tracks_artists)
    users = relationship("User", secondary=users_tracks, back_populates="tracks")




    def __init__(self, name, uri) -> None:
        super().__init__()
        self.name = name
        self.uri = uri

    def __repr__(self) -> str:
        return super().__repr__()


    
    

