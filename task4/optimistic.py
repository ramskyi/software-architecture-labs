import hazelcast
import logging
from time import sleep

logging.basicConfig(level=logging.CRITICAL)

client = hazelcast.HazelcastClient(cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"])
dist_map = client.get_map("my-distributed-map").blocking()

key = "1"
value = 0
dist_map.put_if_absent(key, value)

for _ in range(1000):
    while True:
        old_value = dist_map.get(key)
        new_value = old_value
        sleep(0.01)
        new_value += 1
        if dist_map.replace_if_same(key, old_value, new_value):
            break

client.shutdown()
