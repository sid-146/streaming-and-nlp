from src.kafka.producer.producer_factory import KafkaProducerFactory
from src.db.mongodb.mongodb_factory import MongoDBFactory
from src.common.config_loader import load_config

import json
import ijson
import time


def run():
    # Todo: Update kafka config yaml to handle each unique producer case
    kafka_config = load_config("kafka.yaml")
    mongo_config = load_config("mongo.yaml")
    topic = "test_topic"
    config = {}
    config["bootstrap.servers"] = ",".join(kafka_config["kafka"]["bootstrap_servers"])
    config["client.id"] = "yelp_review_producer"
    producer = KafkaProducerFactory.create_producer(**config)
    mongo_client = MongoDBFactory.create_mongodb_client(**config)

    with open("data/yelp_academic_dataset_review.json", "r") as f:
        reviews = ijson.items(f, "", multiple_values=True)
        for review in reviews:
            producer.produce(
                topic=topic,
                key=str(review["review_id"]),
                value=json.dumps(review).encode("utf-8"),
                callback=KafkaProducerFactory.delivery_report,
            )
            producer.poll(0)
            time.sleep(5)
    producer.flush()


if __name__ == "__main__":
    run()
