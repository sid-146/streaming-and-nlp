from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDBFactory:
    @staticmethod
    def create_mongo_collection_client(config: dict) -> Collection:
        client = MongoClient(
            config["host"],
            config["port"],
            username=config["username"],
            password=config["password"],
        )
        return client[config["database"]][config["collection"]]

    @staticmethod
    def create_mongodb_client(config) -> MongoClient:
        client = MongoClient(
            config["host"],
            config["port"],
            username=config["username"],
            password=config["password"],
        )
        return client[config["database"]]


if __name__ == "__main__":
    mongo_client = MongoDBFactory.create_mongo_collection_client()
