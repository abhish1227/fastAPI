from .. import models, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import engine, get_db
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    db_user = db.query(models.Users).filter(
        models.Users.email == user.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The provided credentials does not exist! Please try again."
        )

    if not utils.validate_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Incorrect password! Please try again."
        )

    access_token = oauth2.create_access_token(
        data={"user_id": db_user.id})

    return {"access_token": access_token, "token_type": "Bearer"}
