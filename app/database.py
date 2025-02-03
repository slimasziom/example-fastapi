from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DB_URL = f'postgresql://{settings.db_username}:{settings.db_pwd}@{settings.db_host}:{settings.db_port}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

      
# retries = 0
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', 
#             database='fastapi', 
#             user='postgres', 
#             password='postgres', 
#             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print(f"Database connection was succesfull")
#         break
    
#     except Exception as error:
#         print(f"Connecting to db failed, error: {error}")
#         retries += 1
        
#         if retries > 5:
#             break
        
#         time.sleep(2)