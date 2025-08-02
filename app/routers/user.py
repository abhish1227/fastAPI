from .. import models, schemas, utils
from ..database import engine, get_db
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    search_email = db.query(models.Users).filter(
        models.Users.email == user.email).first()
    if search_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email id: {user.email} already exists!"
        )

    hashed_password = utils.hash(user.password)
    user.password = hashed_password  # Hash the password before saving

    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found!"
        )

    return user.first()
