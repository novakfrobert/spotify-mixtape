from sqlalchemy.sql.functions import mode
from Services.PlaylistCreatorService import PlaylistCreatorService
from Database.UnitOfWork import UnitOfWork
from fastapi_utils.cbv import cbv
from router import router
from Services.SpotifyDataService import SpotifyDataService
from Models.User import User



@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class UsersController: 

    def __init__(self):
        self.Service = SpotifyDataService()
        self.PlaylistCreatorService = PlaylistCreatorService()
        self.UnitOfWork = UnitOfWork()

    @router.get('/model/me')
    def get_current_user_info(self):

        spotify_user = self.Service.get_current_user_info()

        name = spotify_user['display_name']
        spotify_id = spotify_user['id']
        model_user = User(name, "", spotify_id)

        db_user = self.UnitOfWork.get_user_by_spotify_id(spotify_id)

        if db_user is not None:
            db_user.is_saved = True
            return db_user

        return model_user


    @router.get('/model/get/users')
    def get_users_like(self, query: str):
        model_users = self.PlaylistCreatorService.get_users_like(query)
        return model_users


    

        

