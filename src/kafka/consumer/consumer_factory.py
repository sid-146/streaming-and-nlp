from confluent_kafka import Consumer
import json


class KafkaConsumerFactory:
    @staticmethod
    def create_consumer(topic: str, config: dict) -> Consumer:
        return Consumer(
            topic=topic,
            **config,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            enable_auto_commit=False,
            auto_offset_reset="earliest",
        )
