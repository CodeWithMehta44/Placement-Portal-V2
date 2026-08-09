import redis

cache = redis.Redis(
    host="localhost",
    port=6379,
    db=1,
    decode_responses=True
)


def clear_job_cache():
    keys = cache.scan_iter("jobs:*")

    for key in keys:
        cache.delete(key)

    print("JOB CACHE CLEARED")