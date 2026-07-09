import os

from dotenv import load_dotenv
from langgraph.checkpoint.redis import AsyncRedisSaver

load_dotenv()

REDIS_URL = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}"

redis_context = None
checkpointer = None


async def initialize_checkpointer():

    global redis_context
    global checkpointer

    if checkpointer is None:

        redis_context = AsyncRedisSaver.from_conn_string(
            REDIS_URL,
            ttl={
                "default_ttl": 60 * 24 * 7,   # 7 days (minutes)
                "refresh_on_read": True,
            },
        )

        checkpointer = await redis_context.__aenter__()

        await checkpointer.asetup()

    return checkpointer


async def shutdown_checkpointer():

    global redis_context

    if redis_context:

        await redis_context.__aexit__(
            None,
            None,
            None,
        )