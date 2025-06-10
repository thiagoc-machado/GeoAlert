import redis
import time

def wait_for_redis(timeout=10):
    r = redis.Redis(host='localhost', port=6379, db=0)
    start = time.time()
    while True:
        try:
            r.ping()
            print('✅ Redis pronto!')
            return
        except redis.exceptions.ConnectionError:
            if time.time() - start > timeout:
                raise TimeoutError('❌ Redis não respondeu após {} segundos'.format(timeout))
            time.sleep(0.5)

if __name__ == '__main__':
    wait_for_redis()
