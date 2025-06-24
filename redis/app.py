import redis

r = redis.Redis(host="localhost", port=6380, db=0)
# r.set('test_key1', 'hello')
print(r.get("test_key").decode())
