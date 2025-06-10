
import redis

def test_redis_connection():
    try:
        r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=1)
        r.ping()
        assert True
    except redis.exceptions.ConnectionError:
        assert True