import  pytest

from app.core.celery_app import fetch_url
from app.core.celery_app import celery_app, add



@pytest.mark.asyncio
async def test_fetch_url():
    """
    测试 Celery 任务 fetch_url 是否可以正常执行。
    """
    tasks = [fetch_url.delay('www.example.com/test') for _ in range(1)]


@pytest.mark.asyncio
def test_add_eager():
    # 临时设置为 eager 模式
    # celery_app.conf.update(task_always_eager=True)
    # celery_app.conf.update(task_eager_propagates=True)

    celery_app.conf.update(task_always_eager=True)

    result = add.delay(4, 6)
    assert result.get() == 10

