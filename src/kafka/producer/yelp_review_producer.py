from src.kafka.producer.producer_factory import KafkaProducerFactory
from src.db.mongodb.mongodb_factory import MongoDBFactory
from src.common.config_loader import load_config
from src.common.mongo_functions import query_checkpoint
from src.common.helper import json_serializer

import json
import ijson
import time
import random


def run():
    # Todo: Update kafka config yaml to handle each unique producer case
    kafka_config = load_config("kafka.yaml")["kafka"]["producers"][
        "yelp_review_producer"
    ]
    mongo_config = load_config("mongo.yaml")["checkpoints_db"]
    topic = kafka_config["topic"]
    config = {}
    config["bootstrap.servers"] = ",".join(kafka_config["bootstrap_servers"])
    config["client.id"] = "yelp_review_producer"
    producer = KafkaProducerFactory.create_producer(**config)
    mongo_collection_client = MongoDBFactory.create_mongo_collection_client(
        mongo_config
    )
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
        record = mongo_collection_client.find_one(filter={"_id": record.inserted_id})

    checkpoint = record["idx"]  # records done till now
    print("Skipping till checkpoint idx: ", checkpoint)

    with open("data/yelp_academic_dataset_review.json", "r") as f:
        reviews = ijson.items(f, "", multiple_values=True)
        for idx, review in enumerate(reviews):
            if idx < checkpoint:
                continue

            print(review)

            producer.produce(
                topic=topic,
                key=str(review["review_id"]).encode("utf-8"),
                value=json.dumps(review, default=json_serializer).encode("utf-8"),
                callback=KafkaProducerFactory.delivery_report,
            )
            producer.poll(0)

            mongo_collection_client.update_one(
                filter={"process_name": "yelp_review_producer"},
                update={
                    "$set": {
                        "last_processed_review_id": review["review_id"],
                        "timestamp": time.time(),
                        "idx": idx,
                    }
                },
            )
            checkpoint = idx
            sleep_timer = (
                random.randint(
                    kafka_config["time_range_ms"]["min"],
                    kafka_config["time_range_ms"]["max"],
                )
                / 1000
            )
            time.sleep(sleep_timer)
            break

    producer.flush()


if __name__ == "__main__":
    run()
