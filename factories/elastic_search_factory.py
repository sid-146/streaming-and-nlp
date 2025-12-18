from elasticsearch import Elasticsearch


class ElasticSearchFactory:
    @staticmethod
    def create_esclient(config: dict) -> Elasticsearch:
        return Elasticsearch(**config)
