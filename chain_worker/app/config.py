import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일의 환경 변수를 로드

# Redis 및 Celery 설정
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://redis_queue:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://redis_queue:6379/0")
