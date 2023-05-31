from Services.PlaylistCreatorService import PlaylistCreatorService
from Database.UnitOfWork import UnitOfWork
from fastapi_utils.cbv import cbv
from router import router
from Models.Track import Track
from Models.User import User
import time



@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class TracksController: 

    def __init__(self):
        self.Service = PlaylistCreatorService()

    @router.get('/model/tracks/me/save')
    def save_tracks(self):
        user = self.Service.save_current_user_info()
        self.Service.save_tracks(user)


    @router.get('/model/fromspotify/tracks/me/')
    def get_my_tracks_from_spotify(self):
        return self.Service.get_all_my_spotify_tracks_as_model()

    @router.get('/model/fromdb/tracks/{spotify_id}/')
    def get_tracks_by_spotify_id(self, spotify_id: str):
        res = self.Service.get_tracks_by_spotify_id(spotify_id)
        return res
