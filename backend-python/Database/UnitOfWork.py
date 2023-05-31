from Models.Artist import Artist
from Database.Repository import Repository
from database_creation import Session, engine
from Models.Track import Track
from Models.User import User
from sqlalchemy.orm import joinedload

class UnitOfWork:

    def __init__(self):
        self.Session = Session()
        self.Tracks = Repository(self.Session, Track)
        self.Users = Repository(self.Session, User)
        self.Artists = Repository(self.Session, Artist)

    def commit(self):
        self.Session.commit()


    def save_or_get_user(self, user):
        db_user = self.Users.get().filter_by(spotify_id=user.spotify_id).first()

        if db_user is None:
            self.Users.add(user)
            self.commit()
            return user

        return db_user

    def get_user_by_spotify_id(self, spotify_id):
        return self.Users.get().filter_by(spotify_id=spotify_id).first()

    def get_tracks_by_user_spotify_id(self, spotify_id):
        return self.Tracks.get().filter(Track.users.any(spotify_id=spotify_id)).options(joinedload(Track.artists)).all()

    def get_artists_by_user_spotify_id(self, spotify_id):
        return self.Artists.get().filter(Track.users.any(spotify_id=spotify_id)).all()

    def get_artist_by_name(self, name):
        return self.Artists.get().filter_by(name=name).first()

    def get_track_by_name(self, name):
        return self.Tracks.get().filter_by(name=name).first()

    def get_users_like(self, query):
        query = query+"%"
        return self.Users.get().filter(User.name.like(query)).all()


    def add_users_tracks(self, tracks, user):

        new = 0
        old = 0
        for track in tracks:

            db_track = self.Tracks.get().filter_by(name=track.name).first()

            if db_track is None: 
                print("new track")
                new += 1
                self.Tracks.add(track)
            else:
                old += 1
                db_track.users.append(user)

        print("old tracks ", old)
        print("new tracks ", new)
        self.commit()
        
