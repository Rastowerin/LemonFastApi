from sqlalchemy import Column, Integer, String

from app.database import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    position = Column(Integer, nullable=False, unique=True)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)
    views = Column(Integer, nullable=False)
