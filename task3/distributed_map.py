import hazelcast
import logging


logging.basicConfig(level=logging.CRITICAL)

client = hazelcast.HazelcastClient(cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"])

dist_map = client.get_map("my-distributed-map").blocking()

for i in range(1000):
    dist_map.put(f"{i}", f"{i}")

client.shutdown()
