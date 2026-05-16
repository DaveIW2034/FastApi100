# 基准测试示例
import time
import json
import msgpack
import ujson

data = {'task_id': '12345', 'args': [1, 2, 3], 'kwargs': {'key': 'value'}, 'result': list(range(1000))}

# JSON 标准库
start = time.time()
for _ in range(10000):
    serialized = json.dumps(data)
    deserialized = json.loads(serialized)
json_time = time.time() - start

# msgpack
start = time.time()
for _ in range(10000):
    serialized = msgpack.packb(data)
    deserialized = msgpack.unpackb(serialized)
msgpack_time = time.time() - start

# ujson
start = time.time()
for _ in range(10000):
    serialized = ujson.dumps(data)
    deserialized = ujson.loads(serialized)
ujson_time = time.time() - start

print(f"JSON: {json_time:.2f}s")      # ~1.00x (基准)
print(f"msgpack: {msgpack_time:.2f}s") # ~0.60x (快40%)
print(f"ujson: {ujson_time:.2f}s")    # ~0.40x (快60%)



# 测试数据
test_data = {
    'task': 'app.tasks.process_data',
    'args': list(range(100)),
    'kwargs': {'batch_size': 1000, 'timeout': 30},
    'metadata': {'timestamp': '2024-01-01T00:00:00', 'version': '1.0'}
}

json_size = len(json.dumps(test_data))
msgpack_size = len(msgpack.packb(test_data))
ujson_size = len(ujson.dumps(test_data))

print(f"JSON: {json_size} bytes")      # 基准大小
print(f"msgpack: {msgpack_size} bytes") # 通常小20-40%
print(f"ujson: {ujson_size} bytes")    # 与JSON相同

if __name__ == "__main__":
    pass
