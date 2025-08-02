
# creating access token
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import EmailStr
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Function to create a JWT access token, by encoding the user data and setting an expiration time.


def create_access_token(data: dict):
    to_encode = data.copy()

    # Set the expiration time for the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # updating the expiration time in the data
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        retrieved_id: str = payload.get("user_id")

        if retrieved_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=str(retrieved_id))

    except JWTError:
        raise credentials_exception

    return token_data

# we can pass this as a dependency to any of our desired endpoints to verify the user


# setting dependency on the login end-point so that it retrieves the login data from there
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials.", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user
