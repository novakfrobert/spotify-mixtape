from time import sleep
from fastapi import FastAPI
from router import router
import uvicorn
from database_creation import Base, engine
from fastapi.middleware.cors import CORSMiddleware


def create_db_mapping():
    from Models.User import User
    from Models.Tracks_Artists import tracks_artists
    from Models.Track import Track
    from Models.Artist import Artist
    Base.metadata.create_all(engine)



def start_rest_server():
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8080",
    ]

    from Controllers.Authentication import AuthenticationController
    from Controllers.SpotifyController import SpotifyController
    from Controllers.TracksController import TracksController
    from Controllers.UsersController import UsersController

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    create_db_mapping()
    start_rest_server()

