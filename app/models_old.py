from sqlalchemy import column, Integer, String, Boolean
from .database_old import Base

class Post(Base):
    __tablename__ = "posts"
    id = column(Integer, primary_key=True, nullable=False)
    name = column(String, nullable=False)
    content = column(String, nullable=False)
    published = column(Boolean, default=True)