# FastApi100

一个基于 `FastAPI`、`SQLAlchemy Async`、`MySQL`、`Celery` 和 `Redis` 的 Python 后端示例项目。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动依赖服务

项目本地运行依赖 MySQL 和 Redis，可使用：

```bash
docker compose up -d mysql redis
```

默认数据库连接为：

```text
mysql+aiomysql://root:root@localhost:3306/testdb
```

也可以通过环境变量 `DATABASE_URL` 覆盖。

## 启动项目

主应用入口为 `app/main.py`，当前 FastAPI app 对象为 `app.main:app`。

```bash
python -m app.main
```

默认会启动在 `0.0.0.0:8000`。

## 运行测试

运行全部测试：

```bash
pytest
```

按文件运行：

```bash
pytest test/test_trace_middleware.py
pytest test/test_celery.py
pytest test/test_connection_pool.py
```

说明：

- `test/test_connection_pool.py` 依赖本地 MySQL 可用。
- `test/test_celery.py` 可能依赖 Redis 或 Celery 配置。
- `test/test_trace_middleware.py` 适合作为快速回归检查。
