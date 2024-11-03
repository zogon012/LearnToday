from .db.session import get_db
from .repositories.user import UserRepository
from .services.user import UserService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository=repository)
