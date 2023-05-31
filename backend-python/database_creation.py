from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database

print("Init db...")

engine = create_engine('mysql+pymysql://webadmin:m1n1Motorway$@localhost:3306/spotify-playlist-creator3')

# Create database if it does not exist.
if not database_exists(engine.url):
    create_database(engine.url)
else:
    # Connect the database if exists.
    engine.connect()

connection = engine.connect()
Base = declarative_base()

Session = sessionmaker(bind=engine)



