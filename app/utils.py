from passlib.context import CryptContext
pwd_context = CryptContext(schemes="Bcrypt",deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)