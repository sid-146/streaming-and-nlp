from src.kafka.producer.producer_factory import KafkaProducerFactory
from src.db.mongodb.mongodb_factory import MongoDBFactory
from src.common.config_loader import load_config
from src.common.mongo_functions import query_checkpoint

import json
import ijson
import time


def run():
    # Todo: Update kafka config yaml to handle each unique producer case
    kafka_config = load_config("kafka.yaml")
    mongo_config = load_config("mongo.yaml")["checkpoints_db"]
    topic = "test_topic"
    config = {}
    config["bootstrap.servers"] = ",".join(kafka_config["kafka"]["bootstrap_servers"])
    config["client.id"] = "yelp_review_producer"
    producer = KafkaProducerFactory.create_producer(**config)
    mongo_collection_client = MongoDBFactory.create_mongo_collection_client(mongo_config)
    record = query_checkpoint(mongo_collection_client, "yelp_review_producer")

    # means no records with this are present.
    if record is None:
        record = mongo_collection_client.insert_one(
            {
                "process_name": "yelp_review_producer",
                "last_processed_review_id": None,
                "timestamp": time.time(),
                "idx": -1,
            }
        )

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
