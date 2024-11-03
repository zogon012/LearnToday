from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from my_fastapi_project.api.v1.api import api_router
from my_fastapi_project.core.config import settings
from my_fastapi_project.db.session import init_db

# 애플리케이션 시작시 테이블 생성
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="FastAPI 프로젝트의 API 문서입니다.",
        routes=app.routes,
    )

    # 서버 정보 추가
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["root"])
async def root():
    """
    루트 엔드포인트입니다.
    """
    return {"message": "Welcome to FastAPI Project"}
