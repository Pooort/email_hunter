from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base
from settings import DBCONNECTION

engine = create_engine(DBCONNECTION)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
