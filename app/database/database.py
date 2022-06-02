from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_HOST = "ec2-34-230-153-41.compute-1.amazonaws.com"
DB_USERNAME = "ihctuluduuhqfk"
DB_DATABASE = "d1b0bi7ufeer4e"
DB_PASSWORD = "d652886a2528ad8d525924a4d09dcff13c8c8c4a9f59d4acba1accf3525d4684"
DB_PORT = 5432

engine = create_engine(
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}",
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
