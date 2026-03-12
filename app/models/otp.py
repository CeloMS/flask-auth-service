from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, UTC
from app.database import Base

class Otp(Base):
    __tablename__ = "otp"
    __exclude__ = {'code'}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    code = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    valid_at = Column(DateTime, nullable=False)
    def to_dict(self):
        data = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns if column.name not in self.__exclude__
        }
        return data
