from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker


async def create_broker() -> RedisStreamBroker:
    backend = RedisAsyncResultBackend(redis_url="redis://localhost:6379/0")
    broker = RedisStreamBroker(
        url="redis://localhost:6379/1"
    ).with_result_backend(result_backend=backend)

    return broker
