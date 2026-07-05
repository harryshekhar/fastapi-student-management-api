import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# This gets the URL from Render, or uses your local one as a backup
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:new_secure_password@localhost:5432/studentdb"
)

#render deploy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()