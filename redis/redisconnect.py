import redis

# pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
# r = redis.Redis(connection_pool=pool)
#
# pipe = r.pipeline(transaction=True)
#
# r.set("name", "zhangsan")
# r.set("name", "lisa")
# pipe.execute()
#
# print(r.get("name"))


# class RedisHelpers(object):
#     def __init__(self):
#         self.__conn = redis.Redis(host='127.0.0.1', port=6379)
#         self.channel = 'monitor'
#
#     def publish(self, msg):
#         self.__conn.publish(self.channel, msg)
#         return True
#
#     def subscribe(self):
#         pub = self.__conn.pubsub()
#         pub.subscribe(self.channel)
#         pub.parse_response()
#         return pub

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)
r.set("title", "python")