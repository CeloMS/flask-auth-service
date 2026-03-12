from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit=False
)
Base = declarative_base()

def load_db():
    from app.models.user import User
    from app.models.otp import Otp
    Base.metadata.create_all(bind=engine)