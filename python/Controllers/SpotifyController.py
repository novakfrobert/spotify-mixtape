from Services.PlaylistCreatorService import PlaylistCreatorService
from fastapi_utils.cbv import cbv
from router import router
from fastapi import Request
from Services.SpotifyDataService import SpotifyDataService


@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class SpotifyController: 

    # URLS
    BASE_URL = 'https://api.spotify.com/v1'

    Service = SpotifyDataService()


    def __init__(self) -> None:
        self.Service = SpotifyDataService()
        self.PlaylistCreatorService = PlaylistCreatorService()


    @router.get('/user_info/{user}')
    def get_user_info(self, user):
        """
        """
        return self.Service.get_user_info(user)


    @router.get('/me')
    def get_current_user_info(self):
        """
        """
        return self.Service.get_current_user_info()
        


    @router.get('/me/playlists')
    def get_current_user_playlists(self):
        """
        """
        return self.Service.get_current_user_playlists()


    @router.get('/playlists/{playlist_id}/tracks')
    def get_playlist_tracks(self, playlist_id, limit=100, offset=0):
        """
        """
        return self.Service.get_playlist_tracks(playlist_id, limit, offset)


    @router.get('/playlists/{playlist_id}/tracks/all')
    def get_playlist_tracks_all(self, playlist_id, limit=100, offset=0):
        """
        """
        return self.Service.get_playlist_tracks_all(playlist_id, limit, offset)

    
    @router.get('/me/tracks')
    def get_current_user_tracks(self, limit=50, offset=0):
        """
        """
        return self.Service.get_current_user_tracks(limit, offset)

    @router.get('/me/library/tracks/all')
    def get_all_my_library_tracks(self):
        return self.Service.get_all_my_library_tracks()
            

    @router.get('/me/playlists/tracks/all')
    def get_all_my_playlist_tracks(self):

        return self.Service.get_all_my_playlist_tracks()


    @router.get('/me/tracks/all')
    def get_all_my_tracks(self):
        return self.Service.get_all_my_tracks()

    @router.post('/{user_id}/playlists/create')
    async def create_playlist(self, request: Request, user_id: str):
        body = await request.json()
        name = body['name']
        tracks = body['tracks']
        res = self.Service.create_playlist(name, user_id)
        print(res)
        playlist_id = res['id']
        return self.Service.add_tracks_to_playlist(tracks, playlist_id)
