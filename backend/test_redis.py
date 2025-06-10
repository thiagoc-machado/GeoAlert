import redis

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print('✅ Redis está acessível!')
except redis.ConnectionError as e:
    print('❌ Erro ao conectar no Redis:', e)