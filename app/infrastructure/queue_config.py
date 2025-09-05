from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker


# taskiq worker app.infrastructure.queue_config:broker --fs-discover --tasks-pattern="app/api/tasks.py"
backend = RedisAsyncResultBackend(redis_url="redis://localhost:6379/0")
broker = RedisStreamBroker(
    url="redis://localhost:6379/1"
).with_result_backend(result_backend=backend)
