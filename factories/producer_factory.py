from confluent_kafka import Producer
import json


class KafkaProducerFactory:
    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} : {msg.key()}")

    @staticmethod
    def create_producer(config: dict) -> Producer:
        return Producer(
            config,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )


if __name__ == "__main__":
    print(KafkaProducerFactory.create_producer({"bootstrap.servers": "localhost:9092"}))
