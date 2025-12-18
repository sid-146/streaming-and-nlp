from pymongo import MongoClient


class MongoDBFactory:
    @staticmethod
    def create_mongodb_client(config: dict) -> MongoClient:
        client = MongoClient(config["uri"])
        return client[config["database"]]


if __name__ == '__main__':
    mongo_client = MongoDBFactory.create_mongodb_client()