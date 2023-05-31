from sqlalchemy.sql.functions import mode
from Models.Artist import Artist
from Database.UnitOfWork import UnitOfWork
from Models.User import User
from Models.Track import Track

from Services.SpotifyDataService import SpotifyDataService


class PlaylistCreatorService:

    SpotifyDataService = SpotifyDataService()

    def __init__(self):
        self.SpotifyDataService = SpotifyDataService()
        self.UnitOfWork = UnitOfWork()
        self.Artists = {}
        self.Tracks = {}
        self.User = None


    def save_current_user_info(self):

        spotify_user = self.SpotifyDataService.get_current_user_info()

        name = spotify_user['display_name']
        spotify_id = spotify_user['id']
        model_user = User(name, "", spotify_id)

        self.User = self.UnitOfWork.save_or_get_user(model_user)
        return self.User


    def get_all_my_spotify_tracks_as_model(self):
        spotify_tracks = self.SpotifyDataService.get_all_my_tracks()

        for t in spotify_tracks:
            model_track = self.convert_spotify_track_to_model(t)
            self.Tracks[model_track.name] = model_track

        model_tracks = list(self.Tracks.values())
        print(len(model_tracks))
        return model_tracks


    def get_tracks_by_spotify_id(self, spotify_id):
        return self.UnitOfWork.get_tracks_by_user_spotify_id(spotify_id)
    
    def get_users_like(self, query):
        return self.UnitOfWork.get_users_like(query)

    def save_tracks(self, user):

        saved_tracks = self.UnitOfWork.get_tracks_by_user_spotify_id(user.spotify_id)

        saved_artists = self.UnitOfWork.get_artists_by_user_spotify_id(user.spotify_id)

        for t in saved_tracks:
            self.Tracks[t.name.lower()] = t

        for a in saved_artists:
            self.Artists[a.name.lower()] = a

        spotfy_tracks = self.SpotifyDataService.get_all_my_tracks()
        for t in spotfy_tracks:
            track = self.ensure_track(t, user)

        spotfy_tracks = self.SpotifyDataService.get_all_my_playlist_tracks()
        for t in spotfy_tracks:
            track = self.ensure_track(t, user)

        model_tracks = self.Tracks.values()

        print(len(model_tracks))

        self.UnitOfWork.add_users_tracks(model_tracks, user)

        #return model_tracks


    def convert_spotify_track_to_model(self, spotify_track):
        name = spotify_track['track']['name'].lower()
        uri = spotify_track['track']['uri']
        track = Track(name, uri)

        artists = []

        for a in spotify_track['track']['artists']:
            artist_name = a['name'].lower()
            artist = Artist(artist_name)
            artists.append(artist)

        track.artists = artists
        return track

    def ensure_artist(self, spotify_artist, user):
        name = spotify_artist['name'].lower()

        if name in self.Artists: 
            artist = self.Artists[name]
        else:
            artist = self.UnitOfWork.get_artist_by_name(name)
            if artist is None:
                artist = Artist(name)

            user.artists.append(artist)
            self.Artists[name] = artist

        return artist


    def ensure_track(self, spotify_track, user):
        name = spotify_track['track']['name'].lower()
        uri = spotify_track['track']['uri']
        is_new = False

        if name in self.Tracks:
            track = self.Tracks[name]
        else:
            track = self.UnitOfWork.get_track_by_name(name)
            if track is None:
                is_new = True
                track = Track(name, uri)

                for a in spotify_track['track']['artists']:
                    artist = self.ensure_artist(a, user)
                    track.artists.append(artist)

            track.users.append(user)
            self.Tracks[name] = track

        return track, is_new



       

    
    
