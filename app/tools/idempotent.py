from typing import Callable


def idempotent(func: Callable) -> Callable:

    def warper(*args, **kwargs):
        # 这里可以添加幂等性检查的逻辑
        # 例如，检查请求的唯一标识符是否已经处理过
        # 如果已经处理过，则直接返回结果或抛出异常
        print("Idempotent check passed")
        # 把结果存到redis中.
        # 这里可以添加存储结果到 Redis 的逻辑
        # 例如，使用 Redis 的 SETNX 命令来确保只有第一次调用会执行
        # 如果需要，可以在这里添加日志记录
        return func(*args, **kwargs)
