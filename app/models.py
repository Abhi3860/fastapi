from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import text # We still use text for server_default


class Post(SQLModel, table=True):
    __tablename__ = "posts" # Optional, SQLModel defaults to class name

    # nullable=False is the default for standard types in SQLModel
    id: int = Field(default=None, primary_key=True)
    title: str = Field()
    content: str = Field()
    
    # For server_default we usually rely on the sa_column_kwargs or specific handling,
    # but for simplicity in SQLModel, setting a Python default is often preferred.
    # However, to strictly match the server-side default logic:
    published: bool = Field(
        sa_column_kwargs={"server_default": text("True")}) 
    
    # Handling server-side timestamps exactly like the video:
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