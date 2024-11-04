from app.worker import celery_app


@celery_app.task
def task_b(previous_result):
    print("B 작업 수행 중, 이전 작업 결과:", previous_result)
    # B 작업 수행 로직
    return "B 작업 완료"
