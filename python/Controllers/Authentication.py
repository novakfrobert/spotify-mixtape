import requests
import base64
import json
from urllib.request import urlretrieve
from urllib.parse import urlencode
from common import generate_random_string
from fastapi_utils.cbv import cbv
from starlette.responses import RedirectResponse
from router import router
from state import State

@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class AuthenticationController: 

    # URLS
    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    CLIENT_ID = 'redacted'
    CLIENT_SECRET = 'redacted'

    SCOPE = 'user-read-private user-read-email playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative user-library-read'

    STATE = generate_random_string(16)

    REDIRECT_URI = 'http://localhost:5000/callback'

    def __init__(self):
        pass

    @router.get('/login')
    def getLogin(self):

        options = {
            'client_id': self.CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': self.REDIRECT_URI,
            'scope': self.SCOPE,
            'state': self.STATE
        }

        query_string = urlencode(options)

        auth_url = self.AUTH_URL + "/?" + query_string

        print(auth_url)

        headers = {
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Headers": 'Content-Type,Authorization',
            "Access-Control-Allow-Methods": 'GET,PUT,POST,DELETE,OPTIONS'
        }

        return RedirectResponse(url=auth_url, headers=headers)



    @router.get('/callback')
    def login_callback(self, code: str, state: str):

        auth_code = code
        
        auth_header = base64.urlsafe_b64encode((self.CLIENT_ID + ':' + self.CLIENT_SECRET).encode('ascii'))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic %s' % auth_header.decode('ascii')
        }

        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.REDIRECT_URI
        }

        # Make a request to the /token endpoint to get an access token
        access_token_request = requests.post(url=self.TOKEN_URL, data=payload, headers=headers)

        # convert the response to JSON
        response_data = access_token_request.json()

        print("call back response")
        print(response_data)

        State.ACCESS_TOKEN = response_data['access_token']
        State.REFRESH_TOKEN = response_data['refresh_token']

        return RedirectResponse(url="http://localhost:8080/#/MixtapeMaker")


    @router.get('/refresh_token')
    def refresh_token(self, refresh_token: str):

        auth_header = base64.urlsafe_b64encode((self.CLIENT_ID + ':' + self.CLIENT_SECRET).encode('ascii'))
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic %s' % auth_header.decode('ascii')
        }

        payload = {
                'grant_type': 'authorization_code',
                'refresh_token': refresh_token
                #'client_id': CLIENT_ID,
                #'client_secret': CLIENT_SECRET,
            }

        # Make a request to the /token endpoint to get an access token
        access_token_request = requests.post(url=self.TOKEN_URL, data=payload, headers=headers)

            # convert the response to JSON
        response_data = access_token_request.json()

        State.ACCESS_TOKEN = response_data['access_token']


