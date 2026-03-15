from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, UTC
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    __exclude__ = {'password_hash'}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    validated = Column(Boolean, nullable=False, default=False)

    def to_dict(self):
        data = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns if column.name not in self.__exclude__
        }
        return data