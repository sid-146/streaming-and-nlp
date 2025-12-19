from pymongo import MongoClient


class MongoDBFactory:
    @staticmethod
    def create_mongodb_client(config: dict) -> MongoClient:
        client = MongoClient(
            config["host"],
            config["port"],
            username=config["username"],
            password=config["password"],
        )
        return client[config["database"]][config["collection"]]


if __name__ == "__main__":
    mongo_client = MongoDBFactory.create_mongodb_client()
