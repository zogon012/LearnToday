from typing import List, Optional
from src.repositories.user import UserRepository
from src.models.user import User
from src.schemas.user import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_users(self) -> List[User]:
        return self.repository.get_all()

    def get_user(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def create_user(self, user_create: UserCreate) -> User:
        # 이메일 중복 체크
        if self.repository.get_by_email(user_create.email):
            raise ValueError("Email already registered")

        user = User(name=user_create.name, email=user_create.email)
        return self.repository.create(user)
