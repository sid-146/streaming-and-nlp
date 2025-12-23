from src.kafka.consumer.consumer_factory import KafkaConsumerFactory
from src.db.mongodb.mongodb_factory import MongoDBFactory
from src.common.config_loader import load_config
from src.common.mongo_functions import query_checkpoint
from src.common.helper import json_serializer

import json
import ijson
import time
import random


from confluent_kafka import KafkaException


def run():
    kafka_config = load_config("kafka.yaml")["kafka"]["consumers"][
        "yelp_raw_review_consumer"
    ]
    conf = {
        "bootstrap.servers": ",".join(kafka_config["bootstrap_servers"]),
        "group.id": kafka_config["group_id"],
        "client.id": kafka_config["client_id"],
        "auto.offset.reset": kafka_config["offset"],
        "enable.auto.commit": kafka_config["autocommit"],
        "session.timeout.ms": kafka_config.get("timeout", 10000),
    }

    consumer = KafkaConsumerFactory.create_consumer(conf)
    consumer.subscribe([kafka_config["topic"]])

    raw_review_config = load_config("mongo.yaml")["raw_review_collection"]
    mongo_review_client = MongoDBFactory.create_mongo_collection_client(
        raw_review_config
    )

    # Todo: Create a checkpoint system for the mongodb for raw_reviews using checkpoints collection
    try:
        print("Consumer Started.")
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(msg.error())
                continue

            # Todo: Create script for airflow to perform de-dup on basis of the review.
            # Todo: Keep the latest record only.

            # Decode
            value = json.loads(msg.value().decode("utf-8"))
            value["timestamp"] = time.time()
            # Upload into the raw_review collection
            inserted = mongo_review_client.insert_one(value)
            print(f"Inserted record with _id: {inserted.inserted_id}")
            # Update the checkpoint using consumer.commit(asynchronous=False)
            # consumer.commit(asynchronous=False) # No need of this as autoCommit is enabled in config
            # break

    except Exception as e:
        print(f"Failed with error : {e}")
    finally:
        consumer.close()
