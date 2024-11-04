from app.worker import celery_app


@celery_app.task
def task_a():
    print("A 작업 수행 중...")
    # A 작업 수행 로직
    return "A 작업 완료"
