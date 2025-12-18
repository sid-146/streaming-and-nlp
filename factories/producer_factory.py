from confluent_kafka import Producer


class KafkaProducerFactory:
    @staticmethod
    def create_producer(config: dict) -> Producer:
        return Producer(config)
