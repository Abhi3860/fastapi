from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlmodel import Session
from .. import database, schemas, models, utils
from sqlmodel import select


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    
    user = db.exec(select(models.User).where(models.User.email == user_credentials.email)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    #create and return token
    return{"token":"example token"}