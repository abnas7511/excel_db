from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Connection details
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

# PostgreSQL connection string
DATABASE_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
engine = create_engine(DATABASE_URL, echo=True, pool_size=5, max_overflow=10)
Base = declarative_base()

# FileInfo table definition
class UsrerInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False)
    emailid = Column(String, nullable=False)
    role = Column(String, nullable=False)
    application_mapped = Column(String, nullable=False)
    license_type = Column(String, nullable=False)

# Creating the table
Base.metadata.create_all(engine)

# Creating a session
Session = sessionmaker(bind=engine)
session = Session()