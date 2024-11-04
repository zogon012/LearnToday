from app.tasks.task_a import task_a
from app.tasks.task_b import task_b
from app.tasks.task_c import task_c


def execute_pipeline():
    """작업 A -> 작업 B -> 작업 C의 순차적 실행"""
    chain = task_a.s() | task_b.s() | task_c.s()
    result = chain.apply()  # 동기적으로 실행하여 대기하지 않고 즉시 실행
    print("모든 작업 완료!", result.get())
