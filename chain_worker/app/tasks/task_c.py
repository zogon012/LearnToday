from app.worker import celery_app


@celery_app.task
def task_c(previous_result):
    print("C 작업 수행 중, 이전 작업 결과:", previous_result)
    # C 작업 수행 로직
    return "C 작업 완료"
