from sqlalchemy.sql.elements import True_
from rest import RestRequest
from state import State


class SpotifyDataService:


    # URLS
    BASE_URL = 'https://api.spotify.com/v1'


    def __init__(self):

        default_headers = {
            'Authorization': 'Bearer ' + State.ACCESS_TOKEN
        }

        self.http = RestRequest(self.BASE_URL, default_headers)
    


    def get_user_info(self, user):
        """
        """

        endpoint = "users/" + user

        response = self.http.get(endpoint)

        print(response)

        return response


    def get_current_user_info(self):
        """
        """

        endpoint = "/me"

        response = self.http.get(endpoint)

        print(response.json())

        return response.json()


    def get_current_user_playlists(self):
        """
        """

        endpoint = "/me/playlists"
        response = self.http.get(endpoint)
        return response.json()


    def get_playlist_tracks(self, playlist_id, limit=100, offset=0):
        """
        """

        endpoint = "/playlists/" + playlist_id + "/tracks"
        params = {
            'offset': offset,
            'limit': limit

        }
        response = self.http.get(endpoint, params=params)
        return response.json()


    def get_playlist_tracks_all(self, playlist_id, limit=100, offset=0):
        """
        """
        response = self.get_playlist_tracks(playlist_id)

        tracks = response["items"]
        next = response["next"]

        while next is not None:
            response = self.http.get(url_override=next).json()
            tracks += response["items"]
            next = response["next"]

        return tracks

    
    def get_current_user_tracks(self, limit=50, offset=0):
        """
        """

        endpoint = "/me/tracks"
        params = {
            'offset': offset,
            'limit': limit

        }
        response = self.http.get(endpoint, params=params)
        return response.json()


    def get_all_my_library_tracks(self):

        response = self.get_current_user_tracks()
        tracks = response["items"]
        next = response["next"]

        while next is not None:
            response = self.http.get(url_override=next).json()
            tracks += response["items"]
            next = response["next"]

        return tracks
            

    def get_all_my_playlist_tracks(self):

        first_response = self.get_current_user_playlists()
        user = self.get_current_user_info()
        user_id = user["id"]

        tracks = []

        for playlist in first_response["items"]:

            id = playlist["id"]
            owner = playlist["owner"]["id"]

            # If this isn't a playlist by the logged in user, skip it
            if owner != user_id: 
                print(owner)
                continue

            print("Processing playlist: " + playlist["name"])

            tracks += self.get_playlist_tracks_all(id)

        return tracks


    def get_all_my_tracks(self):
        tracks = {}

        spotfy_tracks = self.get_all_my_library_tracks()
        #spotfy_tracks = self.get_current_user_tracks()['items']
        for t in spotfy_tracks:
            name = t["track"]["name"]
            tracks[name] = t

        spotfy_tracks = self.get_all_my_playlist_tracks()
        for t in spotfy_tracks:
            name = t["track"]["name"]
            tracks[name] = t

        return tracks.values()


    def create_playlist(self, name, user_id):
        endpoint = '/users/' + user_id + '/playlists'
        body = {
            'name': name,
            'public': True,
            'description': 'A mixtape created by Bobbie\'s playlist creator'
        }
        response = self.http.post(endpoint, payload=body)
        return response.json()


    def add_tracks_to_playlist(self, tracks, playlist_id):
        endpoint = '/playlists/' + playlist_id + '/tracks'

        uris = [t['uri'] for t in tracks]

        while len(uris) > 0:
            
            uri_section = uris[:100]
            del uris [:100]
            body = {
                'uris': uri_section,
            }
            response = self.http.post(endpoint, payload=body)
        return response.json()

