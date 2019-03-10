import json
import random
import time

from kafka import KafkaProducer

# Kafka broker connection string
KAFKA_BROKER = "localhost:9092"

# Kafka topic to produce to
TOPIC = "purchase_stream_topic"

import logging


class Generate:
    """Kafka test data generator

    count: number of messages to send
    pause_time: time in seconds to pause between messages
    """

    def __init__(self, count=10, pause=0.1):
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
        self.count = count
        self.pause_time = pause

    @staticmethod
    def _generate_rand_purchase():
        """Create random purchase data"""
        category = random.choice(["baked_goods", "coffee"])
        purchase_price = round(random.uniform(1.75, 8.50),2)
        sales_tax = round(purchase_price * 0.085, 2)
        return {"category": category, "price": purchase_price, "tax": sales_tax}

    def _produce(self, msg):
        print(msg)
        self.producer.send(TOPIC, json.dumps(msg).encode("utf-8"))

    def start(self):
        for _ in range(self.count):
            message = self._generate_rand_purchase()
            self._produce(message)
            if self.pause_time > 0:
                time.sleep(self.pause_time)
        self.producer.flush()


if __name__ == "__main__":
    g = Generate(count=1000, pause=-1)
    g.start()
