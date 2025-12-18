from src.kafka.producer.producer_factory import KafkaProducerFactory
from src.common.config_loader import load_config

import json

# This is testing code; remove with actual logic
import time


def run():
    # Todo: Update kafka config yaml to handle each unique producer case
    kafka_config = load_config("kafka.yaml")
    topic = "test_topic"
    config = {}
    config["bootstrap.servers"] = ",".join(kafka_config["kafka"]["bootstrap_servers"])
    config["client.id"] = "yelp_review_producer"
    producer = KafkaProducerFactory.create_producer(**config)
    for i in range(20):
        message = {
            "review_id": f"review_{i}",
            "text": f"This is review number {i}",
        }

        producer.produce(
            topic=topic,
            key=str(message["review_id"]),
            value=json.dumps(message).encode("utf-8"),
            callback=KafkaProducerFactory.delivery_report,
        )
        producer.poll(0)
        time.sleep(5)
    producer.flush()


if __name__ == "__main__":
    run()
