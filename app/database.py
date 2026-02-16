from sqlmodel import create_engine, Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Hellrider3860@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#dependency
def get_db():
    with Session(engine) as session:
        yield session