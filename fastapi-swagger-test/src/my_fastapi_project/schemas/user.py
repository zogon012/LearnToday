from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., description="사용자의 이름", example="홍길동")
    email: EmailStr = Field(
        ..., description="사용자의 이메일 주소", example="user@example.com"
    )


class UserCreate(UserBase):
    """새로운 사용자를 생성할 때 사용되는 스키마"""

    pass


class User(UserBase):
    """데이터베이스에서 조회된 사용자 정보를 반환할 때 사용되는 스키마"""

    id: int = Field(..., description="사용자의 고유 ID", example=1)

    class Config:
        from_attributes = True
