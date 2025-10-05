# This script sets up our database connection using SQLAlchemy.
# What: It creates a SQLAlchemy engine, which manages connections to the database. SessionLocal is a factory for creating new database session objects. The get_db function is a dependency that we will use in our API endpoints to get a database session and ensure it's properly closed after the request is finished.
# Why: This centralized setup makes our database interactions clean, reusable, and efficient. Connection pooling (pool_size=10, max_overflow=20) is used to manage multiple simultaneous database connections, which is crucial for a web application's performance.


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True, # Checks connections for liveness before use
    pool_size=10, # Number of connections to keep open in the pool
    max_overflow=20 # Number of connections that can be created beyond pool_size
)

# Each instance of the SessionLocal class will be a new database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A base class for our models to inherit from
Base = declarative_base()

def get_db():
    """
    FastAPI dependency to get a database session.
    Yields a session and ensures it's closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close