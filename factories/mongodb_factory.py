from pymongo import MongoClient


class MongoDBFactory:
    @staticmethod
    def create_mongodb_client(uri: str) -> MongoClient:
        return MongoClient(uri)
