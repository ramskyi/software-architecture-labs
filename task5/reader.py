import hazelcast
import logging
from time import sleep

logging.basicConfig(level=logging.CRITICAL)

client = hazelcast.HazelcastClient(cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"])
bounded_q = client.get_queue("my-bounded-queue").blocking()

for _ in range(1000):
    value = bounded_q.take()
    print(f"Value = {value}")
    sleep(0.01)

client.shutdown()
