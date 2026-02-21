from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# configure the database URL here (sqlite for demo)
SQLALCHEMY_DATABASE_URL = "sqlite:///./hackathon.db"

# if using other databases (postgres, mysql), change accordingly
# e.g. "postgresql://user:password@localhost/dbname"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
