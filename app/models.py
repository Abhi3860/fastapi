from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import text # We still use text for server_default


class Post(SQLModel, table=True):
    __tablename__ = "posts" # Optional, SQLModel defaults to class name

    
    id: int = Field(default=None, primary_key=True)
    title: str = Field()
    content: str = Field()
    
   
    published: bool = Field(
        sa_column_kwargs={"server_default": text("True")}) 
    
    
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )

class User(SQLModel, table=True):
    __tablename__="users"
    id: int = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    password:str = Field(nullable=False)
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )