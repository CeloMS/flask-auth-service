from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    __exclude__ = {'password_hash'}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    last_login_at = Column(DateTime, nullable=True)

    def to_dict(self):
        data = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns if column.name not in self.__exclude__
        }
        return data