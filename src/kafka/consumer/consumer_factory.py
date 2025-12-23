from confluent_kafka import Consumer
import json


class KafkaConsumerFactory:
    @staticmethod
    def create_consumer(config: dict) -> Consumer:
        return Consumer(
            **config
        )
