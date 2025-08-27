from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker


backend = RedisAsyncResultBackend(redis_url="redis://localhost:6379/0")
broker = RedisStreamBroker(
    url="redis://localhost:6379/1"
).with_result_backend(result_backend=backend)
