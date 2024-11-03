from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from my_fastapi_project.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# 애플리케이션 시작시 테이블 자동 생성
def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
