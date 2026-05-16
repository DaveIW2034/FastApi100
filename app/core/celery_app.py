# -*- coding: utf-8 -*-
"""
文件: celery_app.py
说明: 初始化 Celery 应用与任务定义，包含基础任务类与示例任务/工作流。
创建时间: 2025-08-19
"""

import time
import logging

import requests
from billiard.exceptions import SoftTimeLimitExceeded

from celery import Celery, Task, chain, group, chord
from celery.bin.result import result
from requests import HTTPError
from sqlalchemy import String

# 创建 Celery 实例
celery_app = Celery(
    'celery_app',  # 项目名
    broker='redis://localhost:6379/0',      # Redis 作为 Broker
    backend='redis://localhost:6379/1'      # Redis 作为结果存储
)

# 可选：加载配置（如果你有 celeryconfig.py）
# app.config_from_object('celeryconfig')

# 基础配置（生产环境建议独立成 celeryconfig.py）
celery_app.conf.update(
    timezone='Asia/Shanghai',          # 时区
    enable_utc=False,                   # 禁用 UTC，使用本地时间
    task_serializer='json',             # 任务序列化格式
    result_serializer='json',           # 结果序列化格式
    accept_content=['json'],             # 接受的内容类型
    result_accept_content=['json'],
    task_track_started=True,             # 启用 STARTED 状态

    # task_acks_late=True,                 # 任务完成后才确认（防丢）
    task_reject_on_worker_lost=True,      # worker 挂掉重新分配任务
    # 并发优化
    worker_concurrency=1,  # 并发 worker 数
    worker_max_tasks_per_child=1000,      # worker 长时间运行后自动重启
    worker_prefetch_multiplier=1,     # worker celery worker默认取任务数量
    # 批量操作任务, 拆分任务.

    result_expires=3600*24, # 24 小时后自动清理.
    # task_time_limit = 60, # 硬时间限制，超过后会抛出 TimeLimitExceeded 异常
    # task_soft_time_limit = 30  # 秒
)


# logging.basicConfig(level=logging.INFO,
#                     format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s')
#
# worker_hijack_root_logger = False  # 避免 Celery 抢占你的日志配置


class BaseTask(Task):

    # time_limit = 60  # 硬时间限制，超过后会抛出 TimeLimitExceeded 异常
    # soft_time_limit = 30  # 软时间限制，超过后会抛出 SoftTimeLimitExceeded 异常


    def on_success(self, retval, task_id, args, kwargs):
        logging.info(f"任务: {self.name} 成功，结果: {retval}")


    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logging.error(f"任务: {self.name} 失败 ： {exc}")
        # 可以存数据库
        # save_task_error_to_db(task_id, self.name, exc, einfo)
        # 或发到 Sentry
        # sentry_sdk.capture_exception(exc)


    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        logging.info(f"任务: {self.name} 成功完成，结果: {result}")
        # 可以存数据库
        # save_task_result_to_db(self.request.id, self.name, result)
        # 或发到 Sentry
        # sentry_sdk.capture_message(f"任务: {self.name} 成功完成，结果: {result}")


# @app.task(ignore_result=True)
# def clear_queues():
#     print("Clearing queues...")
#     print("Queues cleared...")
#     return None
#
#
# scheduler = BackgroundScheduler()
# scheduler.add_job(clear_queues.delay, 'interval', minutes=1)
# scheduler.add_job(clear_queues.delay, 'interval', seconds=1)
#
# scheduler.start()




# @app.task(bind=True, max_retries=3, default_retry_delay=10)  # 最多重试3次，每次间隔10秒
@celery_app.task(base=BaseTask,
                 autoretry_for=(ConnectionError, TimeoutError, HTTPError, Exception),
                 retry_kwargs={'max_retries': 1,  'countdown': 3},
                 retry_backoff=True, # 指数退避，2^n 秒
                 retry_jitter=True,  # 加随机抖动
                 # time_limit = 60, # 硬时间限制, 超过后会抛出 TimeLimitExceeded 异常
                 # soft_time_limit = 30 # 软时间限制，超过后会抛出 SoftTimeLimitExceeded 异常
)
def fetch_url(url):
    # r = requests.get(url, timeout=5)

    # try:
        time.sleep(10)  # 模拟处理时间
    # except SoftTimeLimitExceeded:
    #     print("软时间限制到达, 正在清理...")
    #     return {'status': 'timeout', 'url': url}
    # return {'status': 'ok', 'url': url}


# fetch_url.delay('googl11111e.com')


@celery_app.task(base=BaseTask, bind=True, soft_time_limit=30, time_limit=60)
def resilient_task(self, checkpoint=None):

    print(checkpoint)
    if checkpoint is None:
        checkpoint = 0

    preserve_checkpoint = checkpoint
    try:
        for i in range(checkpoint, 100):
            # 模拟处理任务
            preserve_checkpoint = i
            time.sleep(1)

    except SoftTimeLimitExceeded:
        checkpoint = preserve_checkpoint
        logging.warning(f"任务 {self.request.id} 达到软时间限制，保存检查点 {preserve_checkpoint} 并重新调度。")

        # 重新调度任务从检查点继续
        self.retry(
            countdown=6,
            max_retries=5,
            kwargs={"checkpoint": checkpoint}
        )


# resilient_task.delay(checkpoint=None)


@celery_app.task()
def add(x, y):

    return x + y


@celery_app.task()
def multiply(x, y):
    return x * y


@celery_app.task()
def sub(x, y):

    if isinstance(x, list):
        return [i - y for i in x]
    elif isinstance(x, int):
        return x - y
    else:
        logging.error("类型错误: x should be int or list, y should be int")
        raise TypeError



# 顺序执行 add → multiply → sub
# res = chain(
#     add.s(2, 3),          # 返回 5
#     multiply.s(10),       # 5 * 10 = 50
#     sub.s(20)           # 50 - 20 = 30
# )
# res = res.apply_async()
# logging.info("顺序任务结果: %s", res.get())  # 30


# 并行执行 add 任务
# res = group(
#     add.s(1, 2),  # 返回 3
#     add.s(3, 4),  # 返回 7
#     add.s(5, 6)   # 返回 11
# )
# res.delay()
# res = res.apply_async()
# logging.info("并行任务结果： %s", res.get())  # [3, 7, 11]


# 先并行执行 add 任务，全部完成后执行 sub 任务
# res = chord(group(add.s(1, i) for i in range(5)), sub.s(20))
# res.delay()
# res = res.apply_async()
# logging.info("回调任务结果: %s", res)  # 60, 140, 220






# chain(
#     fetch_url.s(),  # 拉取数据
#     parse_json.s(),  # 解析
#     save_to_db.s()   # 存储
# )()


# cities = ["Beijing", "Shanghai", "Shenzhen"]
#
# job = group(generate_city_report.s(city) for city in cities)
# res = job.apply_async()
#
# all_results = res.get()  # 等待全部完成
# merge_reports(all_results)

















