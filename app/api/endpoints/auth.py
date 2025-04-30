from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.db.session import get_db
from app.services import user as user_service

router = APIRouter()


@router.post("/register", response_model=schemas.User)
def register_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user.
    """
    user = user_service.create_user(db, user_in)
    return user


@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get access token for user authentication.
    """
    user = user_service.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_service.create_user_token(user)


@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    """
    Get current user information.
    """
    return current_user