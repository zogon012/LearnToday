from celery import Celery
from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# Celery 인스턴스 생성
celery_app = Celery(
    "chainworker", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND
)
celery_app.conf.task_routes = {"app.tasks.*": {"queue": "chain_queue"}}

# 작업 모듈 로드
celery_app.autodiscover_tasks(["app.tasks"])
