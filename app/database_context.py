from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
import os

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URI)

Session = scoped_session(sessionmaker(bind=engine,expire_on_commit=False))
Base = declarative_base()
