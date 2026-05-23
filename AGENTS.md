# AGENTS.md

## 目的

本文件定义本仓库的默认协作规范，适用于 AI agent 和人工协作者。
在没有额外说明时，后续分析、修改、测试和提交都应遵循这里的约定。

## 项目概览

- 项目类型：Python 后端示例项目
- 当前主技术栈：`FastAPI`、`SQLAlchemy Async`、`MySQL`、`Celery`、`Redis`、`pytest`
- Python 依赖入口：`requirements.txt`
- 主应用入口：`app/main.py`
- 当前 API app 对象：`app.main:app`

说明：

- 仓库现有 `README.md` 信息很少，默认以代码实际实现和本文件为准。
- 仓库中部分注释与当前实现不完全一致。遇到冲突时，以实际代码行为为准，不要沿用过时注释。

## 默认工作范围

以下目录属于默认维护范围：

- `app/main.py`：应用入口，注册中间件与路由
- `app/api/v1/`：HTTP 路由层
- `app/core/`：数据库、Celery、配置等基础设施代码
- `app/models/`：SQLAlchemy 模型
- `app/schemas/`：Pydantic schema
- `app/middleware/`：请求链路中间件
- `app/tools/`：工具类代码
- `test/`：测试代码
- `docker-compose.yaml`：本地依赖服务编排
- `requirements.txt`：Python 依赖定义

以下目录不在默认维护范围内：

- `app/service_registry_discover/`

对排除目录的处理规则：

- 除非用户明确点名，否则不要分析、修改、重构或补测试。
- 不要把排除目录视为主应用主链路的一部分。
- 不要因为排除目录中的示例实现而影响主应用设计判断。

## 当前应用事实

- `app/main.py` 当前确实创建并导出了 `FastAPI` 应用，不要把它当成“仅脚本入口”。
- 当前注册的路由前缀是 `/api/v1/user`。
- 当前应用接入了 `TraceIDMiddleware`，请求和响应会处理 `X-Trace-Id`。

项目安装、依赖服务启动、应用启动和测试运行方式统一维护在 `README.md`，不要在本文件重复维护一套运行说明。


## FastAPI规则

- 必须 async
- router 禁止操作 DB
- 所有 response 使用 schema

## 编码规则
- 禁止 print
- 必须 logger
- 必须 type hints
- 必须 async
- SQL 不允许字符串拼接


## 分层规则

- router 不允许操作数据库
- 所有 DB 必须走 service
- service 不允许依赖 router

## 错误处理

- 所有异常必须捕获
- API 必须返回统一结构
- 禁止裸 except

## Redis规则

- key 必须带前缀
- 必须设置 TTL
- 禁止大 key

## Redis Review规则

发现以下情况时必须警告：

- 没有 TTL
- 使用 KEYS *
- value 过大
- 没有 prefix
- 阻塞操作
- 热 key 风险


## 测试与验证约定

- 改动 API、schema、数据库访问逻辑时，优先补充或更新对应测试。
- 涉及 `test/test_connection_pool.py` 的验证需要本地 MySQL 可用。
- 涉及 `test/test_celery.py` 的验证可能依赖 Redis 或 Celery 配置；测试前先确认运行模式。
- `test/test_trace_middleware.py` 属于相对独立的应用层测试，适合作为快速回归检查。
- 如果因为环境依赖无法完成某项验证，需要在结果说明里明确写出未验证项和原因。

## 修改约束

- 默认采用最小改动原则，不做无关重构。
- 修改接口行为时，同步检查 `app/api/v1/`、`app/schemas/`、`app/models/` 和测试是否需要联动更新。
- 修改数据库相关逻辑时，优先保持现有异步 SQLAlchemy 用法一致。
- 修改日志、中间件或请求链路时，注意不要破坏 `X-Trace-Id` 的透传与响应头写回。
- 未经用户明确要求，不要顺手修复与当前任务无关的问题。

## 禁止混入的运行产物

以下内容默认视为运行产物或本地噪音，不应作为业务改动提交：

- `__pycache__/`
- `*.pyc`
- `.pytest_cache/`
- 日志文件，例如 `app/logs/info.log`
- Celery 运行产物，例如 `app/core/celerybeat-schedule.*`

如果这些文件出现在工作区变更中：

- 不要把它们当成需要维护的业务文件。
- 不要围绕这些文件做功能性修改。
- 除非用户明确要求，否则不要把它们纳入提交范围。

## 协作建议

- 在开始较大改动前，先确认是否影响主入口 `app/main.py` 或用户接口 `/api/v1/user`。
- 如果发现仓库中的注释、文档、容器说明与代码实现冲突，先记录“当前真实行为”，再决定是否修正文档。
- 对不确定是否属于主链路的目录或脚本，优先参考本文件的范围定义，而不是按目录名称自行推断。
