import redis


r = redis.Redis()
#r.set('Croatia','gdrg')
a = r.get("Croatia").decode("utf-8")
print(a)
