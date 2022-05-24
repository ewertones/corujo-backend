import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_SOCKET_DIR = "cloudsql"
# DB_INSTANCE_CONNECTION_NAME = "corujo:us-central1:corujo-db"

pool = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL.create(
        drivername="postgresql+pg8000",
        username=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        # query={
        #     # "unix_sock": f"{DB_SOCKET_DIR}/{DB_INSTANCE_CONNECTION_NAME}/.s.PGSQL.5432"  # .format(                ,  # e.g. "/cloudsql"                 )  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
        # },
    )
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pool)
Base = declarative_base()
